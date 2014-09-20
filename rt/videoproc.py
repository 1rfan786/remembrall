import subprocess, datetime, sys, base64, requests, os, json
import cv2
import pika

PROC_FPS = 0.5
MAXDIM = 800 # Rekognition API resolution limit

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='files_queue', durable=True)

epoch = datetime.datetime.utcfromtimestamp(0)

def get_start(name):
    sp = subprocess.Popen(['exiftool', '-f', '-MediaCreateDate', '-d', '%Y%m%d-%H%M%S', name],
            stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    if sp.wait() != 0:
        raise Exception
    time_str = sp.stdout.read().strip().split()[-1]
    time = datetime.datetime.strptime(time_str, '%Y%m%d-%H%M%S')
    return long((time - epoch).total_seconds()) * 1000

def process(name):
    name = os.path.join(os.getcwd(), '../run/data', name)
    start = get_start(name)
    cap = cv2.VideoCapture(name)
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    step = max(1, int(fps / PROC_FPS))
    while cap.isOpened():
        ms = cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
        ms_since_epoch = start + long(ms)
        ret, img = cap.retrieve()
        height, width, depth = img.shape
        scaleFactor = min(float(MAXDIM) / height, float(MAXDIM) / width)
        newHeight, newWidth = int(height * scaleFactor), int(width * scaleFactor)
        img = cv2.resize(img, (newWidth, newHeight))
        if ret:
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
                print matches
        if not all(cap.grab() for i in xrange(step)):
            break
    cap.release()

def callback(ch, method, properties, body):
    print ' [x] Received %r' % body
    process(body)
    print ' [x] Done'
    ch.basic_ack(delivery_tag = method.delivery_tag)

def main():
    print ' [x] Waiting for messages. To exit press CTRL+C'
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback,
            queue='files_queue')
    channel.start_consuming()

if __name__ == '__main__':
    main()