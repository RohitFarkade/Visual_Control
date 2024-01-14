# Foundings



# What To Learn?


## (Necessary) ✅
#### MediaPipe Hands:

- Hands solution functionalities, configuration options
Landmark detection, understanding data structures
- Drawing landmarks, accessing specific landmark coordinates
- MediaPipe Hands documentation and tutorials
#### PyAutoGUI:

- Mouse and keyboard control capabilities
- Triggering clicks, scrolls, keyboard presses
- Exploring PyAutoGUI documentation and examples
#### Gesture Recognition Basics:

- Analyzing hand landmark data (distances, angles, ratios)
- Implementing basic gesture recognition functions (e.g., "pinch")
- Mapping gestures to PyAutoGUI actions

#### Gesture Tracking:

- Understanding hand movement tracking concepts
- Implementing basic gesture tracking for smoother interactions
- Resources: Tutorials and projects demonstrating gesture tracking


## Advance Topics/Problems(Future Not Urgent) ⏩
#### Multi-touch Handling:

- Recognizing gestures with multiple hands
-Implementing logic for interacting with different windows
#### Advanced Gesture Sequences:

- Training models for recognizing sequences of gestures
- Enabling complex commands through hand movements

# How🔰?

### Simple Approach :-

Distance And Landmark Based

cons:
- Only Simple Gesture
- No Multigesture Support
- Decision Only Based On Single Thresold 

### lil Advance Approach:-
Training A ml model to recognize custom gesture and multihand gesture
(For Traning Purpose We Can implement SVM Or Random Forest)
- but lil difficult


# Two Approches Found



## Beginner Approach:

- Start with the provided checklist and focus on implementing basic gestures.

- Use  available libraries like MediaPipe and PyAutoGUI.

- Consider the "two-finger pinch" example as a starting point and explore similar simple gestures.

- Concentrate on user experience and feedback to refine  application.


## lil Advance approach:

- Explore gesture tracking with tools like MediaPipe's Hand Landmarks to improve smoothness.

- Experiment with machine learning models like SVMs for more complex gesture recognition.

- Focus on a specific set of functionalities based on  project scope.


# Template For Code(Base Code)/Sample Code
```python
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




```


# Resourses
## MediaPipe Hands:

Official Documentation:
- MediaPipe Hands: https://github.com/google/mediapipe/blob/master/docs/solutions/hands.md
- python API Examples: https://medium.com/@aliceheimanxyz/recognize-hand-landmarks-using-google-mediapipe-and-opencv-9ca0a052ce75
- Tutorials and Projects:
Hand Gesture Controlled Webpage with Python and MediaPipe: https://developers.google.com/mediapipe/solutions/vision/hand_landmarker/python
- Real-time Hand Gesture Recognition with Python and MediaPipe: https://www.youtube.com/watch?v=qAw5tuYgVec


## PyAutoGUI:

Official Documentation:
- PyAutoGUI: https://pyautogui.readthedocs.io/
- Blog Posts and Tutorials:
Ultimate Guide to Python PyAutoGUI: https://automatetheboringstuff.com/
- Using PyAutoGUI for Automation: https://towardsdatascience.com/how-to-easily-automate-your-keyboard-to-do-tasks-in-python-b698e98a5c40


![alt text](https://github.com/RohitFarkade/Project/blob/main/image.jpg?raw=true)