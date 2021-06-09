import cv2
import threading

class CarCamera(threading.Thread):
    def __init__(self, threadID, camera_id, daemon=False):
        super().__init__(daemon=daemon)
        self.threadID = threadID
        self._id = camera_id
        self.camera = cv2.VideoCapture(self._id)

    def run(self):
        while True:
            _, frame = self.camera.read()
            cv2.imshow("frame"+str(self._id), frame)
            if cv2.waitKey(100) & 0xff == ord('q'):
                break

    def stop(self):
        self.camera.release()
