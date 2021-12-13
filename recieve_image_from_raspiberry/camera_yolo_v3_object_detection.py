import cv2 as cv
import numpy as np
# import torch
import os
import time
import argparse
yolo_dir= '/Users/haitianhang/Documents/yolov3'
weightsPath=os.path.join(yolo_dir,'yolov3.weights')
# print(weightsPath)
configPath=os.path.join(yolo_dir,'yolov3.cfg')
# print(configPath)
labelsPath=os.path.join(yolo_dir,'coco.names')
# print(labelsPath)
CONFIDENCE=0.5 
THRESHOLD=0.4
# net = cv.dnn.readNet("yolov3.weights", "yolov3.cfg")
net = cv.dnn.readNet(weightsPath,configPath)

with open(labelsPath, 'rt') as f:
    labels=f.read().rstrip('\n').split('\n')
COLORS=np.random.randint(0,255,size=(len(labels),3),dtype="uint8")
# print(labels)

def getOutputsNames(net):
# Get the names of all the layers in the network
    layersNames = net.getLayerNames()
# Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

def yolo_v3_object_detection(img):
    blobImg=cv.dnn.blobFromImage(img,1.0/255.0,(416,416),None,True,False)
    net.setInput(blobImg)
    # outInfo=net.getUnconnetedOutLayersNames()
    outInfo=getOutputsNames(net)
    layerOutPuts=net.forward(outInfo)
    (H,W)=img.shape[:2]

    boxes=[]
    confidences=[]
    classIDs=[]

    for out in layerOutPuts:
        for detection in out:
            scores=detection[5:]
            classID=np.argmax(scores)
            confidence=scores[classID]
            if confidence > CONFIDENCE:
                box=detection[0:4]*np.array([W,H,W,H])
                (centerX,centerY,width,height)=box.astype("int")
                x=int(centerX-(width/2))
                y=int(centerY-(height/2))
                boxes.append([x,y,int(width),int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)
    idxs=cv.dnn.NMSBoxes(boxes,confidences,CONFIDENCE,THRESHOLD)
    lbs=[]
    if len(idxs) > 0:
        for i in idxs.flatten():
            lbs.append(labels[classIDs[i]])

    
    return idxs,boxes,confidences,classIDs,lbs


if __name__ == '__main__':
    cap=cv.VideoCapture(0)
    while(1):
        ret,frame=cap.read()
        # cv.imshow("color",frame)
        # #  first convert into gray scale picture, and then do gaussian blur, and finally use canny edge detection to detect edges
        # img_gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        # cv2.imshow("Gray",img_gray)
        # img_gb=cv2.GaussianBlur(img_gray,(5,5),0)
        # cv2.imshow("GaussianBlur",img_gb)
        # edges=cv2.Canny(img_gb,10,90)
        # cv2.imshow("edge",edges)
        indexs,boxes,confidences,classIDs,lbs=yolo_v3_object_detection(frame)
        # print(indexs)
        if len(indexs) > 0:
            for i in indexs.flatten():
                (x,y)=(boxes[i][0],boxes[i][1])
                (w,h)=(boxes[i][2],boxes[i][3])
                color=[int(c) for c in COLORS[classIDs[i]]]
                cv.rectangle(frame,(x,y),(x+w,y+h), color,2) # width of the line is 2px
                text="{}: {:.4f}".format(lbs[i],confidences[i])
                cv.putText(frame,text,(x,y-5),cv.FONT_HERSHEY_SIMPLEX,0.5,color,2)# size of the text 0.5
        cv.imshow('object detection result',frame)

        if cv.waitKey(1) & 0xFF ==ord('q'):
            break
    cap.release()
    cv.destroyAllWindows
