from operator import truediv
from turtle import distance
import cv2
from cvzone.HandTrackingModule import HandDetector
from grpc import Status
from matplotlib.pyplot import draw


class DragRect():
    def __init__(self, Poscenter, size=[100,100]):
        self.posCenter = Poscenter
        self.size = size
        self.is_locked = False

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size
        if cx-w//2<cursor[0]<cx+w//2 and cy-h//2<cursor[1]<cy+h//2:
            self.posCenter = cursor
            self.is_locked = True



cap = cv2.VideoCapture(0)

detector = HandDetector(detectionCon=0.8)

rect_list = []
for i in range(3): # make shape to move 
    rect_list.append(DragRect([i*130+150,150]))


while True:
    success, image = cap.read()
    image = detector.findHands(image, False)
    lmList, _  = detector.findPosition(image, draw=False)


    if lmList:
        l, _, _ = detector.findDistance(8, 12, image, draw=False)
        if l<30:
            cursor = lmList[8]
            for rect in rect_list:
                rect.update(cursor) # check hand for move
                if rect.is_locked == True: # chedck if hand moving a shape then don't move another shape in same time
                    rect.is_locked = False
                    break
            

    for rect in rect_list: # move shape
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(image, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), (255,255,255), 2) 
        
        

    cv2.imshow('main', image)
    cv2.waitKey(1)


cap.release()
cv2.destroyAllWindows()