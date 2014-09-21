import subprocess, datetime, sys, base64, requests, os, json
import cv2
import pika
from elasticsearch import Elasticsearch
from pydub import AudioSegment
import tempfile


PROC_FPS = 0.5
MAXDIM = 800 # Rekognition API resolution limit

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='files_queue', durable=True)

es = Elasticsearch()

epoch = datetime.datetime.utcfromtimestamp(0)

def get_start(name):
    sp = subprocess.Popen(['exiftool', '-f', '-ContentCreateDate', '-d', '%Y%m%d-%H%M%S', name],
            stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    if sp.wait() != 0:
        raise Exception
    time_str = sp.stdout.read().strip().split()[-1]
    time = datetime.datetime.strptime(time_str, '%Y%m%d-%H%M%S')
    return time

def process(name):
    fullname = os.path.join(os.getcwd(), '../flask_app/static/data', name)
    start = get_start(fullname)
    cap = cv2.VideoCapture(fullname)
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    step = max(1, int(round(fps / PROC_FPS)))
    while cap.isOpened():
        ms = cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
        fn = int(round(cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)))
        frametime = start + datetime.timedelta(0, 0, 1000 * ms)
        ret, img = cap.retrieve()
        height, width, depth = img.shape
        scaleFactor = min(float(MAXDIM) / height, float(MAXDIM) / width)
        newHeight, newWidth = int(height * scaleFactor), int(width * scaleFactor)
        img = cv2.resize(img, (newWidth, newHeight))
        data = cv2.imencode('.png', img)[1]
        encoded = base64.encodestring(data)
        params = {
            'api_key': 'MlNqKOB0gvIJ9dBz',
            'api_secret': 'CWf5gIEQqoo59fRy',
            'jobs': 'scene_understanding_3',
            'base64': encoded
        }
        resp = requests.request('POST', 'https://rekognition.com/func/api/', data = params)
        if resp.status_code == 200:
            content = json.loads(resp.content)
            matches = content['scene_understanding']['matches']
            store = {'matches': matches, 'time': frametime, 'filename': name}
            idn = '%s-%dV' % (frametime.strftime('%Y%m%d-%H%M%S'), fn)
            es.index(index = 'rememberall', doc_type = 'frame', id = idn, body = store)
            print ' [x] Processed %s' % idn
        if not all(cap.grab() for i in xrange(step)):
            break
    cap.release()

def audio(name):
    fullname = os.path.join(os.getcwd(), '../flask_app/static/data', name)
    start = get_start(fullname)
    ft = name.split('.')[-1]
    print fullname, ft
    pre_audio = AudioSegment.from_file(fullname, ft)
    i = 0;
    while i < len(pre_audio):
        frametime = start + datetime.timedelta(0, i / 1000)
        idn = '%s-%dA' % (frametime.strftime('%Y%m%d-%H%M%S'), i / 1000)
        curr_seg = pre_audio[i: i+9000]
        f = tempfile.NamedTemporaryFile(mode="rw+b", delete=True)
        curr_seg.export(f.name, format="wav")
        data = f.read()
        resp = requests.post(url='https://api.wit.ai/speech', data=data, headers={"Authorization": "Bearer BYQ2VNUDCWPSHZPYIPLTZVVEA4PZSB3Y", "Content-Type": "audio/wav"})
        if resp.status_code == 200:
            content = json.loads(resp.content)
            text = content['_text']
            store = {'time': frametime, 'filename': name, 'text': text}
            if text != '':
                es.index(index = 'rememberall', doc_type = 'frame', id = idn, body = store)
                print ' [x] Processed %s' % idn
        i += 9000

def callback(ch, method, properties, body):
    print ' [x] Received %r' % body
    process(body)
    print ' [x] Image Done'
    audio(body)
    print ' [x] Audio Done'
    ch.basic_ack(delivery_tag = method.delivery_tag)

def main():
    print ' [x] Waiting for messages. To exit press CTRL+C'
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback,
            queue='files_queue')
    channel.start_consuming()

if __name__ == '__main__':
    main()
