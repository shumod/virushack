import cv2
import numpy as np
blurThresh=100
def someFrame(newFrame,oldFrame):
    if newFrame.size ==0:
        return "New frame is empty."
    min_valNew, max_valNew, min_locNew, max_loc = cv2.minMaxLoc(newFrame)
    if max_valNew==0:
         return "Frame is black."
    if oldFrame.size ==0:
        return "Old frame is empty."
    min_valOld, max_valOld, min_locOld, max_loc = cv2.minMaxLoc(oldFrame)
    if max_valOld==0:
         return "Frame is black."
    if (min_valNew==0 and min_valOld==0):
        if (min_locNew[0]==min_locOld[0]==min_locNew[1]==min_locOld[1]):
            return "Camera has a broken pixel."
    grayNew = cv2.cvtColor(newFrame, cv2.COLOR_BGR2GRAY)
    grayOld = cv2.cvtColor(oldFrame, cv2.COLOR_BGR2GRAY)
   
    blurNew = np.var( cv2.Laplacian( cv2.cvtColor(grayNew, cv2.COLOR_BGR2GRAY), cv2.CV_64F))
    blurOldF = np.var( cv2.Laplacian( cv2.cvtColor(grayOld, cv2.COLOR_BGR2GRAY), cv2.CV_64F))
    if np.abs(blurNew-blurOldF)<blurThresh:
        return "Camera blurs."
    return "Camera ok."
