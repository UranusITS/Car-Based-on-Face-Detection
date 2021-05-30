import cv2


class FaceDetector:
    def __init__(self, video=0, cascade_classifier_file='haarcascade_frontalface_default.xml',
                 debug=False):
        self._capture = cv2.VideoCapture(video, cv2.CAP_DSHOW)
        self._classifier = cv2.CascadeClassifier(cascade_classifier_file)
        self._debug = debug

    def get_face_pos(self):
        ret, frame = self._capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        face = self._classifier.detectMultiScale(gray, 1.1, 3, cv2.CASCADE_FIND_BIGGEST_OBJECT, (175, 175))
        if self._debug:
            print(face)
        if not isinstance(face, tuple):
            x, y, w, h = face[0]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow('camera', frame)
            return x, y, (w + h) // 2, True
        else:
            cv2.imshow('camera', frame)
            return None, None, None, False

    def release(self):
        self._capture.release()
