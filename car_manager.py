import cv2
import socket
from face_detector import FaceDetector


class CarManager:
    def __init__(self, min_dx=20, min_da=20, init_num=10, debug=False,
                 socket_host='172.18.22.12', socket_port=1919):
        # Init face detection on camera
        self._face_detector = FaceDetector(debug=debug)
        self._min_dx = min_dx
        self._min_da = min_da
        self._init_num = init_num
        self._debug = debug
        self._x = int()
        self._a = int()
        self.init_face()
        # Init socket connection to car
        self._socket_host = socket_host
        self._socket_port = socket_port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._socket.connect((self._socket_host, self._socket_port))
            print('Socket connection accepted')
        except socket.timeout:
            print('Socket connection timeout')
            exit(1)

    def init_face(self):
        print('Print \'s\' to start initialization')
        while True:
            self._face_detector.get_face_pos()
            if cv2.waitKey(5) & 0xFF == ord('s'):
                break
        print('Init face position')
        for i in range(self._init_num):
            x, y, a, fd = self._face_detector.get_face_pos()
            while not fd:
                x, y, a, fd = self._face_detector.get_face_pos()
            self._x += x
            self._a += a
        self._x //= self._init_num
        self._a //= self._init_num
        print('Init finished')

    def run(self):
        while True:
            x, y, a, fd = self._face_detector.get_face_pos()
            if fd:
                # print(x, y, a)
                if a - self._a > self._min_da:
                    self.accelerate()
                elif self._a - a > self._min_da:
                    self.decelerate()
                if x - self._x > self._min_dx:
                    self._x = x
                    self.turn_left()
                elif self._x - x > self._min_dx:
                    self._x = x
                    self.turn_right()
            if cv2.waitKey(5) & 0xFF == 27:
                break
        self.stop()

    def stop(self):
        self._socket.send(str.encode('disconnect', 'ASCII'))
        self._socket.close()
        self._face_detector.release()
        cv2.destroyAllWindows()

    def accelerate(self):
        self._socket.send(str.encode('accel', 'ASCII'))
        if self._debug:
            print('Accelerate')

    def decelerate(self):
        self._socket.send(str.encode('decel', 'ASCII'))
        if self._debug:
            print('Decelerate')

    def turn_left(self):
        self._socket.send(str.encode('left', 'ASCII'))
        if self._debug:
            print('Turn Left')

    def turn_right(self):
        self._socket.send(str.encode('right', 'ASCII'))
        if self._debug:
            print('Turn Right')
