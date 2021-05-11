import cv2
from face_detector import FaceDetector


class CarManager:
    def __init__(self, min_dx=20, min_da=20, debug=False):
        self._face_detector = FaceDetector()
        self._min_dx = min_dx
        self._min_da = min_da
        self._debug = debug

    def run(self):
        x, y, a, fd = self._face_detector.get_face_pos()
        while not fd:
            x, y, a, fd = self._face_detector.get_face_pos()
        while True:
            xx, yy, aa, fd = self._face_detector.get_face_pos()
            if fd:
                if aa - a > self._min_da:
                    self.accelerate()
                elif a - aa > self._min_da:
                    self.decelerate()
                if xx - x > self._min_dx:
                    self.turn_left()
                elif x - xx > self._min_dx:
                    self.turn_right()
                x, y, a = xx, yy, aa
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
        self.stop()

    def stop(self):
        self._face_detector.release()
        cv2.destroyAllWindows()

    def accelerate(self):
        if self._debug:
            print('Accelerate')

    def decelerate(self):
        if self._debug:
            print('Decelerate')

    def turn_left(self):
        if self._debug:
            print('Turn Left')

    def turn_right(self):
        if self._debug:
            print('Turn Right')
