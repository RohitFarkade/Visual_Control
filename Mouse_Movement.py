import cv2 as cv
import mediapipe as mp
import time
import pyautogui as pg
import math

# My Functions

def No_Hands():
    Initial_Time = time.time()


def FCircle(x,y,rad,color):
    cv.circle(img, (x,y), rad, color, cv.FILLED)

def Circle(x,y,rad,color, thick):
    cv.circle(img, (x,y), rad, color, thick)

def mouse_position(nx,ny,cx,cy):
    tx,ty = cx,cy
    rx = tx-nx
    ry = ty-ny
    crX,crY = pg.position()
    x = rx + crX
    y = ry + crY

    return  x,y

# Colors
Red = (0,0,255)
Blue = (255,0,0)
Green = (0,255,0)

# Image Related Variables
h,w,c = 0,0,0

# Pixels Related Variables
cx,cy= 0,0
nx = 0
ny = 0

# Open CV variables
cap = cv.VideoCapture(0)

# Mediapipe Variables
mpHands = mp.solutions.hands
Hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

# Time Related Variables
Initial_Time = time.time()
Current_Time = time.time()
overall_time = 0

# Area Related Variables
Neutral_Area = False
Rad50_Area = False
Rad80_Area = False
Rad125_Area = False

# Angle Variables
angle = 0
slope = 0
Rangle = 0

L,U,R,D = False,False,False,False
Quad1,Quad2,Quad3,Quad4 = False,False,False,False

pg.FAILSAFE = False
while True:

    if Neutral_Area == False:
        if (R and U) and Neutral_Area == False:
            Quad1 = True
            Quad2 = False
            Quad3 = False
            Quad4 = False

            mx,my = mouse_position(nx,ny,cx,cy)
            pg.moveTo(mx,my)
        if L and U and Neutral_Area == False:
            Quad1 = False
            Quad2 = True
            Quad3 = False
            Quad4 = False
            mx, my = mouse_position(nx, ny, cx, cy)
            pg.moveTo(mx, my)


        if L and D and Neutral_Area == False:
            Quad1 = False
            Quad2 = False
            Quad3 = True
            Quad4 = False
            mx, my = mouse_position(nx, ny, cx, cy)
            pg.moveTo(mx, my)


        if R and D and Neutral_Area == False:
            Quad1 = False
            Quad2 = False
            Quad3 = False
            Quad4 = True
            mx, my = mouse_position(nx, ny, cx, cy)
            pg.moveTo(mx, my)


    ret, img = cap.read()
    img = cv.flip(img, 1)
    rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    result = Hands.process(rgb)

    if result.multi_hand_landmarks == None:
        # No_Hands()
        Initial_Time = time.time()
        Neutral_Area = True

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            Current_Time = time.time()
            overall_time = int(Current_Time - Initial_Time)

            index = handLms.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
            h, w, c = img.shape
            cx, cy = int(index.x * w), int(index.y * h)
            Circle(cx, cy, 5, Green, 3)

            if overall_time <= 2:
                nx, ny = cx, cy
            if overall_time >= 2:
                Circle(nx,ny,18,Red, 2)
                Circle(nx,ny,50, Red, 1)
                Circle(nx,ny,80, Red, 1)
                Circle(nx,ny,125, Red, 1)
                cv.line(img, (nx-125,ny),(nx+125,ny), Green, 2)
                cv.line(img, (nx,ny-125),(nx,ny+125), Green, 2)

                if abs(cx - nx) <= 18 and abs(cy - ny) <= 18:
                    Neutral_Area = True
                elif abs(cx - nx) <= 50 and abs(cy - ny) <= 50:
                    Neutral_Area = False
                    pass
                    # print("Area 50")
                elif abs(cx - nx) <= 80 and abs(cy - ny) <= 80:
                    Neutral_Area = False
                    pass
                    # print("Area 80")
                elif abs(cx - nx) <= 125 and abs(cy - ny) <= 125:
                    Neutral_Area = False


            if cx - nx <= 125 and cx - nx >= 0:
                R = True
                L = False
            if cx - nx <= 0 and cx - nx >= -125:
                L = True
                R = False
            if cy - ny <= 125 and cy - ny >= 0:
                D = True
                U = False
            if cy - ny <= 0 and cy - ny >= -125:
                U = True
                D = False


    cv.imshow("Navigation With Radius",img)
    if cv.waitKey(1) == 27:
        break

cap.release()
cv.destroyAllWindows()