from this import d
from traceback import print_tb
import cv2
import mediapipe as mp 
import math


cap = cv2.VideoCapture(0)
pic = cv2.imread('a.jpg')

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

a, b = 150, 150
e, f = 250, 150

while True:
    success, image = cap.read()
    cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resualt = hands.process(rgb_image)
    h , w , c = image.shape

    cv2.rectangle(image, (a-50,b-50), (a+50,b+50), (250,250,250), -1)
    cv2.rectangle(image, (e-50,f-50), (e+50,f+50), (50,50,50), -1)

    if resualt.multi_hand_landmarks:
        for i in resualt.multi_hand_landmarks:
            lm = i.landmark
            cx8, cy8 = int(lm[8].x*w), int(lm[8].y*h)
            cx4, cy4 = int(lm[4].x*w), int(lm[4].y*h)
            distance = int(math.hypot(cx8-cx4, cy8-cy4))

            if distance <= 20:
                if a - 50 < cx4 < a + 50 and a - 50 < cx8 < a + 50 and b - 50 < cy4 < b + 50 and b - 50 < cy8 < b + 50:
                    a = cx4
                    b = cy4
                elif e - 50 < cx4 < e + 50 and e - 50 < cx8 < e + 50 and f - 50 < cy4 < f + 50 and f - 50 < cy8 < f + 50:
                    e = cx4
                    f = cy4

    cv2.imshow('main', image)
    cv2.waitKey(1)
