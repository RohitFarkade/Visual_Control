import pyautogui as pg
import time
import cv2 as cv
import mediapipe as mp

def DrawC(x,y,r):
    cv.circle(img, (x,y),r,(100,79,255), cv.FILLED)

def PutT(text):
    cv.putText(img, text, (50,50), 1, cv.FONT_HERSHEY_DUPLEX, (0, 0, 255), 2)



cap = cv.VideoCapture(0)

mpHands = mp.solutions.hands
Hands = mpHands.Hands(max_num_hands=1)
mpdraw = mp.solutions.drawing_utils
I_Time = time.time()


# Variables
NeutralArea = False
WorkArea = False
R = False
L = False
U = False
D = False

while True:
    ret, img = cap.read()
    img = cv.flip(img, 1)
    rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    if (R and U) and NeutralArea == False:
        print(" 0 to 90 ")
    if R and D and NeutralArea == False:
        print(" 270 to 360")
    if L and U and NeutralArea == False:
        print(" 90 to 180 ")
    if L and D and NeutralArea == False:
        print(" 180 to 270 ")

    result = Hands.process(rgb)

    if result.multi_hand_landmarks == None:
        PutT("Error 404")
        I_Time = time.time()
        NeutralArea = False
        WorkArea = False
        drawing_circle = False
        L,U,R,D = False,False,False,False

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:

            C_Time = time.time()
            O_Time = int(C_Time - I_Time)


            index = handLms.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
            h, w, c = img.shape
            cx, cy = int(index.x * w), int(index.y * h)


            if O_Time <= 2:
                PutT(str("Initializing The Index in " + str(O_Time)))
            if O_Time == 2:
                N_X, N_Y = int(index.x * w), int(index.y * h)
            if O_Time > 2:
                DrawC(N_X, N_Y, 25)
                cv.circle(img, (N_X,N_Y), 50, (200,0,200))
                cv.circle(img, (N_X,N_Y), 80, (200,0,200))
                cv.circle(img, (N_X,N_Y), 125, (200,0,200))


                if (cx-N_X <= 28 and cx-N_X >= -28) and (cy-N_Y <=28 and cy-N_Y >= -28):
                    NeutralArea = True
                    WorkArea = False

                elif (cx-N_X <= 125 and cx-N_X >= -125) and (cy-N_Y <=125 and cy-N_Y >= -125):
                    NeutralArea = False
                    WorkArea = True

            if WorkArea:
                if cx - N_X <= 125 and cx - N_X >=0:
                    R = True
                    L = False
                if cx - N_X <= 0 and cx - N_X >=-125:
                    L = True
                    R = False
                if cy - N_Y <= 125 and cy - N_Y >=0:
                    D = True
                    U = False
                if cy - N_Y <= 0 and cy - N_Y >=-125:
                    U = True
                    D = False

            cv.circle(img, (cx, cy), 5, (0, 255, 0), cv.FILLED)
            # mpdraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cv.imshow("navigation", img)

    if cv.waitKey(1) == 27:
        break

cap.release()
cv.destroyAllWindows()