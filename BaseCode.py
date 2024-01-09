import cv2
import mediapipe as mp
import pyautogui

# Simple Implementation of Pinch Gesture
def recognize_two_finger_pinch(hand_landmarks):
    """Detects a two-finger pinch gesture."""
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

    # Calculate distance between index finger and thumb tips
    distance = ((index_finger_tip.x - thumb_tip.x)**2 +
                (index_finger_tip.y - thumb_tip.y)**2)**0.5

    # Set a threshold for the pinch gesture
    threshold = 0.04  # Adjust as needed

    if distance < threshold:
        return True  # Pinch gesture detected
    else:
        return False
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)  # Use 0 for default webcam

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Process image using MediaPipe
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Draw hand landmarks and implement gesture recognition/actions here
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )
    cv2.imshow('Hand Gesture Control', image)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
          if recognize_two_finger_pinch(hand_landmarks):
              pyautogui.click()  # Trigger mouse click
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

