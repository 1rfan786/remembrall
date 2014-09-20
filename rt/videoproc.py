import subprocess, datetime, sys
import cv2

PROC_FPS = 0.5

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
    start = get_start(name)
    cap = cv2.VideoCapture(name)
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    step = max(1, int(fps / PROC_FPS))
    while cap.isOpened():
        ms = cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
        ms_since_epoch = start + long(ms)
        ret, img = cap.retrieve()
        if ret:
            print ms, ms_since_epoch
            pass # do something with img
        if not all(cap.grab() for i in xrange(step)):
            break
    cap.release()

def main():
    process(sys.argv[1])

if __name__ == '__main__':
    main()
