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
ix,iy= 0,0
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
TandI, IandM, MandR, RandP,MandT= False,False,False,False,False

measurer = 25

pg.FAILSAFE = False
while True:

    if Neutral_Area == False:
        if (R and U) and Neutral_Area == False:
            Quad1 = True
            Quad2 = False
            Quad3 = False
            Quad4 = False

            mx,my = mouse_position(nx, ny, ix, iy)
            pg.moveTo(mx,my)
        if L and U and Neutral_Area == False:
            Quad1 = False
            Quad2 = True
            Quad3 = False
            Quad4 = False
            mx, my = mouse_position(nx, ny, ix, iy)
            pg.moveTo(mx, my)


        if L and D and Neutral_Area == False:
            Quad1 = False
            Quad2 = False
            Quad3 = True
            Quad4 = False
            mx, my = mouse_position(nx, ny, ix, iy)
            pg.moveTo(mx, my)


        if R and D and Neutral_Area == False:
            Quad1 = False
            Quad2 = False
            Quad3 = False
            Quad4 = True
            mx, my = mouse_position(nx, ny, ix, iy)
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
            thumb = handLms.landmark[mpHands.HandLandmark.THUMB_TIP]
            pinky = handLms.landmark[mpHands.HandLandmark.PINKY_TIP]
            middle = handLms.landmark[mpHands.HandLandmark.MIDDLE_FINGER_TIP]
            ring = handLms.landmark[mpHands.HandLandmark.RING_FINGER_TIP]
            h, w, c = img.shape
            ix, iy = int(index.x * w), int(index.y * h)
            mx,my = int(middle.x * w), int(middle.y * h)
            tx,ty = int(thumb.x * w), int(thumb.y *h)
            px,py = int(pinky.x * w), int(pinky.y *h)
            rx, ry = int(ring.x * w), int(ring.y * h)

            if abs(int((ix - tx)+(ty - iy))/2) < measurer: TandI = True
            else: TandI = False
            if abs(int((mx - ix)+(iy - my))/2) < measurer: IandM = True
            else: IandM = False
            if abs(int((rx - mx)+(ry - my))/2) < measurer: MandR = True
            else: MandR = False
            if abs(int((px - rx)+(py - ry))/2) < measurer: RandP = True
            else: RandP = False
            if abs(int((rx - tx) + (ty - ry)) / 2) < measurer:
                MandT = True
            else:
                MandT = False

            Circle(ix, iy, 5, Green, 3)
            leftdistance = ((ix - tx) + (ty - iy)) / 2
            rightdistance = mx - ix
            scrollup = ((px - tx) + (ty - py)) / 2
            scrolldown = ((rx - tx) + (ty - ry)) / 2
            if overall_time <= 2:
                nx, ny = ix, iy
            if overall_time >= 2:
                Circle(nx,ny,18,Red, 2)
                Circle(nx,ny,50, Red, 1)
                Circle(nx,ny,80, Red, 1)
                Circle(nx,ny,125, Red, 1)
                cv.line(img, (nx-125,ny),(nx+125,ny), Green, 2)
                cv.line(img, (nx,ny-125),(nx,ny+125), Green, 2)

                if abs(ix - nx) <= 18 and abs(iy - ny) <= 18:
                    Neutral_Area = True
                elif abs(ix - nx) <= 50 and abs(iy - ny) <= 50:
                    Neutral_Area = False
                    pass
                    # print("Area 50")
                elif abs(ix - nx) <= 80 and abs(iy - ny) <= 80:
                    Neutral_Area = False
                    pass

                elif abs(ix - nx) <= 125 and abs(iy - ny) <= 125:
                    Neutral_Area = False
                else:
                    pass


                if MandT and TandI == False and IandM == False:
                    time.sleep(0.1)
                    pg.rightClick(pg.position())

                elif TandI and MandT == False and IandM == False:
                    time.sleep(0.1)
                    pg.leftClick(pg.position())

                elif TandI == False and IandM == True and MandR== True and RandP==True:
                    # Neutral_Area = True
                    if tx < px:
                        nx, ny = ix, iy
                        pg.scroll(-100)
                    if tx > px:
                        nx, ny = ix, iy
                        pg.scroll(100)

                if IandM and TandI == False and MandR == False:
                    nx, ny = ix, iy


            if ix - nx <= 125 and ix - nx >= 0:
                R = True
                L = False
            if ix - nx <= 0 and ix - nx >= -125:
                L = True
                R = False
            if iy - ny <= 125 and iy - ny >= 0:
                D = True
                U = False
            if iy - ny <= 0 and iy - ny >= -125:
                U = True
                D = False


    cv.imshow("Navigation With Radius",img)
    if cv.waitKey(1) == 27:
        break

cap.release()
cv.destroyAllWindows()