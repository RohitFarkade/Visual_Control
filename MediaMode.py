import time
import cv2 as cv
import pyautogui as pg
import mediapipe as mp

def Circle(x,y,rad,color, thick):
    cv.circle(img, (x,y), rad, color, thick)

cap = cv.VideoCapture(0)
mpHands = mp.solutions.hands
Hands = mpHands.Hands(max_num_hands=1)
mpdraw = mp.solutions.drawing_utils

TandI, IandM, MandR, RandP = False,False,False,False
hit = False
measurer = 20


init_time = time.time()
c_time = 0
Red = (0,0,255)
Blue = (255,0,0)
Green = (0,255,0)


allDone = 0

while True:
    ret, img = cap.read()
    img = cv.flip(img, 1)
    rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    result = Hands.process(rgb)


    if result.multi_hand_landmarks == None:
        fingers_close = False


    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            h,w,c = img.shape

            # Fingers Define Here
            index = handLms.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
            thumb = handLms.landmark[mpHands.HandLandmark.THUMB_TIP]
            middle = handLms.landmark[mpHands.HandLandmark.MIDDLE_FINGER_TIP]
            ring = handLms.landmark[mpHands.HandLandmark.RING_FINGER_TIP]
            pinky = handLms.landmark[mpHands.HandLandmark.PINKY_TIP]
            wrist = handLms.landmark[mpHands.HandLandmark.WRIST]

            ix,iy = int(index.x*w), int(index.y*h)
            tx,ty = int(thumb.x*w), int(thumb.y*h)
            mx,my = int(middle.x*w), int(middle.y*h)
            rx,ry = int(ring.x*w), int(ring.y*h)
            px,py = int(pinky.x*w), int(pinky.y*h)
            wx, wy = int(wrist.x*w), int(wrist.y*h)


            if abs(int((ix - tx)+(ty - iy))/2) < measurer: TandI = True
            else: TandI = False
            if abs(int((mx - ix)+(iy - my))/2) < measurer: IandM = True
            else: IandM = False
            if abs(int((rx - mx)+(ry - my))/2) < measurer: MandR = True
            else: MandR = False
            if abs(int((px - rx)+(py - ry))/2) < measurer: RandP = True
            else: RandP = False

            if TandI and IandM and MandR and RandP:
                cv.rectangle(img, (20,300), (600,325), Red, 2)
                cv.rectangle(img, (22,302), (ix, 323), Blue, cv.FILLED)
                pg.leftClick(ix*3,1010)
                if hit: hit = False
                if hit == False:
                    hit = True
                allDone += 1
            elif TandI == False and (IandM and MandR and RandP):
                if tx < px: pg.press('j')
                if tx > px: pg.press('l')

            elif IandM and MandR == False:
                if hit:
                    pg.leftClick(1920/2,1080/2)
                    pg.press('k')
                hit = False
                pg.press('down')
            elif (RandP and MandR) and IandM == False:
                if hit:
                    pg.leftClick(1920/2,1080/2)
                    pg.press('k')
                hit = False
                pg.press('up')
            elif TandI: pg.press('k')


    cv.imshow("For_Youtube", img)
    if cv.waitKey(1) == 27:
        break
cap.release()
cv.destroyAllWindows()