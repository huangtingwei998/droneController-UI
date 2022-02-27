import json
import time

from qtpy import QtGui

from detector_tracker import tracker
from detector_tracker.detector import Detector


import cv2
clickX = 0  #全局变量，获取鼠标点击的点
clickY = 0  #全局变量，获取鼠标点击的点
ID=0        #全局变量，跟踪的ID


def loadjson():
    with open("config/start.json", "r") as f:
        dict = json.load(f)
        if dict['choice']=='1':
            video = int(dict['video'])
        else:
            video = dict['video']
        isdetect = int(dict['isdetect'])
        print(isdetect)
    return video,isdetect

def Locationclick(event, x, y, flags, params):
    #鼠标右键单击事件
    if event == cv2.EVENT_RBUTTONDOWN:
        global clickX
        global clickY
        clickX = x
        clickY = y

def clickID(bboxes,clickX,clickY):
    global ID
    flag = False
    for (x1, y1, x2, y2, cls_id, pos_id) in bboxes:
        if x1<clickX<x2 and y1<clickY<y2:
            ID = pos_id
            flag = True
            break
    return flag,ID

def countnum(boxes):
    peoplenum,bicyclenum,carnum,motorcyclenum,busnum,trucknum = 0,0,0,0,0,0
    for x1, y1, x2, y2, lbl, conf in boxes:
        if lbl=='person':
            peoplenum+=1
        elif lbl=='bicycle':
            bicyclenum+=1
        elif lbl=='car':
            carnum+=1
        elif lbl=='motorcycle':
            motorcyclenum+=1
        elif lbl=='bus':
            busnum+=1
        else:
            trucknum+=1

    return "people:"+str(peoplenum)+" "+"bicycle:"+str(bicyclenum)+" "+"car:"+str(carnum)+" "+"motorcycle:"+str(motorcyclenum)+" "+"bus:"+str(busnum)+" "+"truck:"+str(trucknum)


class trackermain:
    def __init__(self):
        self.strnum = ""
        self.flag = False
        self.flag2 = False
        cap = cv2.VideoCapture()
        flag, self.image = cap.read()
    def getstarnum(self):
        return self.strnum
    def getFLAG(self):
        return self.flag
    def getFLAG2(self):
        return self.flag2
    def getimage(self):
        return self.image
    def setimage(self,image):
        self.image = image

    def main(self):
        # 加载配置
        video, isdetect = loadjson()
        # 初始化 yolov5
        detector = Detector()

        # 打开视频
        capture = cv2.VideoCapture(video)
        # capture = cv2.VideoCapture('video-02.mp4')

        while True:
            # 读取每帧图片
            _, im = capture.read()
            if im is None:
                break
                # 软件主窗口不需要检测
            if isdetect == 0:
                self.setimage(im)
            # 获取到视频流了，才能开启到跟踪
            self.flag = True
            # 缩小尺寸，1920x1080->960x540
            im = cv2.resize(im, (960, 540))

            list_bboxs = []
            bboxes = detector.detect(im)
            # 计数
            self.strnum =countnum(bboxes)

            # 如果画面中 有bbox
            if len(bboxes) > 0:

                list_bboxs = tracker.update(bboxes, im)
                flag, ID = clickID(list_bboxs, clickX, clickY)
                # 画框
                output_image_frame = tracker.draw_bboxes(im, list_bboxs, ID, line_thickness=None)
                pass
            else:
                # 如果画面中 没有bbox
                output_image_frame = im
            pass
            # 软件主窗口不需要检测
            if isdetect == 1:
                self.setimage(output_image_frame)
            self.flag2 = True
            cv2.imshow('tracker', output_image_frame)

            cv2.waitKey(1)
            cv2.setMouseCallback('tracker', Locationclick)
            pass

        pass
        capture.release()
        cv2.destroyAllWindows()
        self.flag = False


if __name__ == '__main__':
    trackermain  = trackermain()
    trackermain.main()

