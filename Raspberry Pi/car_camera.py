import cv2
import threading

import numpy as np


class CarCamera(threading.Thread):
    def __init__(self, threadID, camera_ids, daemon=False):
        super().__init__(daemon=daemon)
        self.threadID = threadID
        self._ids = camera_ids
        self.cameras = list()
        self.init_cameras()

    def init_cameras(self):
        for id in self._ids:
            self.cameras.append(cv2.VideoCapture(id))

    def run(self):
        frames = list()
        for camera in self.cameras:
            frames.append(np.zeros((480, 640, 3), dtype=np.uint8))
        while True:
            id = 0
            for camera in self.cameras:
                ret, frame = camera.read()
                if ret:
                    frames[id] = frame
                id += 1
            imgs = np.hstack(frames)
            cv2.imshow('car_camera', imgs)
            if cv2.waitKey(100) & 0xff == ord('q'):
                break

    def stop(self):
        for camera in self.cameras:
            camera.release()
