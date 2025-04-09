import cv2
import mediapipe as mp
import pyautogui
import math

# booleans to set scrolling modes
scroll_up = False
scroll_down = False

# simple math distance formula to detect finger proximity
def distance(coords1, coords2):
    return math.sqrt((coords1[0]-coords2[0])**2 + (coords1[1]-coords2[1])**2)
 

# initialize the media pipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_drawing = mp.solutions.drawing_utils

# Start capturing video from the webcam.
try:
    cap = cv2.VideoCapture(1)
except:
    print("Wrong camera")

cv2.namedWindow("Hand Tracking", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Hand Tracking", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)




while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Flip the frame horizontally for a mirror view.
    frame = cv2.flip(frame, 1)
    # h, w, c = frame.shape
    w, h = pyautogui.size()

    # Convert the BGR image to RGB.
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Calculate the palm center by averaging the coordinates of landmarks:
            # 0: wrist, 5: index finger MCP, 9: middle finger MCP,
            # 13: ring finger MCP, 17: pinky finger MCP.
            indices = [0, 5, 9, 13, 17]

            # Retrieve landmark positions for thumb tip, index tip, and middle tip.
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]

            # Convert normalized coordinates to pixel coordinates.
            thumb_coords = (int(thumb_tip.x * w), int(thumb_tip.y * h))
            index_coords = (int(index_tip.x * w), int(index_tip.y * h))
            middle_coords = (int(middle_tip.x * w), int(middle_tip.y * h))
            ring_coords = (int(ring_tip.x * w), int(ring_tip.y * h))

            palm_x = sum([hand_landmarks.landmark[i].x for i in indices]) / len(indices)
            palm_y = sum([hand_landmarks.landmark[i].y for i in indices]) / len(indices)
            palm_coords = (int(palm_x * w), int(palm_y * h))
            
            # Draw a circle at the computed palm center.
            cv2.circle(frame, palm_coords, 10, (0, 255, 0), -1)

            # Draw a circle (node) at each finger tip.
            cv2.circle(frame, thumb_coords, 5, (0, 255, 0), -1)
            cv2.circle(frame, index_coords, 5, (0, 255, 0), -1)
            cv2.circle(frame, middle_coords, 5, (0, 255, 0), -1)
            cv2.circle(frame, ring_coords, 5, (0, 255, 0), -1)

            ## Draw lines connecting thumb to index and index to middle.
            # cv2.line(frame, thumb_coords, index_coords, (255, 0, 0), 2)
            # cv2.line(frame, index_coords, middle_coords, (255, 0, 0), 2)
            # cv2.line(frame, middle_coords, ring_coords, (255, 0, 0), 2)
            
            # Optionally, draw all hand landmarks for context.
            # mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if distance(index_coords, middle_coords) < 35:
                scroll_up = True
            elif distance(middle_coords, ring_coords) < 35:
                scroll_down = True
                


            if scroll_up:
                pyautogui.scroll(-3, _pause=False)
                color = (0, 0, 255)
            elif scroll_down:
                pyautogui.scroll(3, _pause=False)
                color = (0, 0, 255)
            else:
                color = (255, 0, 0)
                # Move the mouse cursor to the palm center.
                pyautogui.moveTo(index_coords[0], index_coords[1], _pause=False)

                if distance(middle_coords, thumb_coords) < 35:
                    pyautogui.click(_pause=False)
                    print("clicking")
                    print(distance(middle_coords, thumb_coords))

            # Draw lines connecting thumb to index and index to middle.
            cv2.line(frame, thumb_coords, index_coords, (255, 0, 0), 2)
            cv2.line(frame, index_coords, middle_coords, (255, 0, 0), 2)
            cv2.line(frame, middle_coords, ring_coords, (255, 0, 0), 2)
        

        scroll_up = False
        scroll_down = False



    # Display the resulting frame.
    cv2.imshow("Hand Tracking", frame)

    # Press 'q' key to exit.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
