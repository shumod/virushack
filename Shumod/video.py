import requests
import cv2

class Checks():
    def __init__(self, source):
        self.source = source

    def testDevice(self):
        cap = cv2.VideoCapture()
        cap.setExceptionMode(True)
        try:
            cap.open(self.source)
        except:
            return False
        else:
            return True
            #
            # # Делаем снимок
            # ret, frame = cap.read()
            #
            # # Записываем в файл
            # cv2.imwrite('cam.png', frame)
            #
            # # Отключаем камеру
            # cap.release()

# check = Checks(source = 'rtsp://192.168.88.252:4747/video')
# check.testDevice())


# try:
#     cap = cv2.VideoCapture('http://192.168.88.252:4747/video')
# except:
#     print (2)
# print (cap.isOpened())
# while (cap.isOpened()):
#     while True:
#         ret, img = cap.read()
#         cv2.imshow('img', img)
#         if cv2.waitKey(30) & 0xff == ord('q'):
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()
# else:
#     print("Alert ! Camera disconnected")