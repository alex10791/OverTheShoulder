
import cv2
import sys
import time
import signal
import overlay
import threading
from parse_config import parse_config, CameraConfig

def signal_handler(sig, frame):
        app.quit()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def main(window, config=CameraConfig()):
    while True:

        s, img = cam.read()

        if s:    # frame captured without any errors
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags = cv2.CASCADE_SCALE_IMAGE
            )

            print(len(faces))

            if len(faces) == 1:
                window.disable_noise()
            else:
                window.enable_noise()

            time.sleep(config.capture_interval)


if __name__ == "__main__":
    filename = None

    if len(sys.argv) > 2:
        print("Usage: %s [ots.conf]" % sys.argv[0])
        exit(1)
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    config = parse_config(filename)

    # face detection Haar
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # initialize the camera
    cam = cv2.VideoCapture(config.camera.id)   # 0 -> index of camera
    if cam is None or not cam.isOpened():
       print('Warning: unable to open video source: ', config.camera.id)
       exit(1)

    # create overlay and detection thread
    window, app = overlay.init()
    t = threading.Thread(target=main, args=(window, config.camera))
    t.daemon = True
    t.start()

    # start overlay window
    overlay.start(window, app)
