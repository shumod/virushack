import cv2
import numpy as np
from collections import OrderedDict 
class Checks():
    def __init__(self, source):
        self.source = source
    stream = cv2.VideoCapture()
    blurThresh=100
    def testDevice(self):        
        self.stream.setExceptionMode(True)
        try:
            self.stream.open(self.source)
        except:
            self.stream.release()
            return False
        else:
            return True
    def testFrames(self):
        count = 0
        while(count<100):
            ret, frame = self.stream.read()
            if ret:                
                if count ==50:
                    oldFrame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if count ==99:
                    newFrame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                count=count+1
        result = OrderedDict({'result':self.someFrame(newFrame,oldFrame)})
        self.stream.release()
        return result
    def someFrame(self,FFrame,SFrame):
        if FFrame.size ==0:
            return "New frame is empty."
        min_valNew, max_valNew, min_locNew, max_loc = cv2.minMaxLoc(FFrame)
        if max_valNew==0:
             return "Frame is black."
        if SFrame.size ==0:
            return "Old frame is empty."
        min_valOld, max_valOld, min_locOld, max_loc = cv2.minMaxLoc(SFrame)
        if max_valOld==0:
             return "Frame is black."
        if (min_valNew==0 and min_valOld==0):
            if (min_locNew[0]==min_locOld[0]==min_locNew[1]==min_locOld[1]):
                return "Camera has a broken pixel."   
        blurF = int(( cv2.Laplacian( FFrame,  cv2.CV_64F)).var())
        blurS = int(( cv2.Laplacian( SFrame, cv2.CV_64F)).var())
        if blurF<self.blurThresh and blurS<self.blurThresh:
            return "Camera blurs."
        return "Camera ok."
