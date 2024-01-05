import mediapipe as mp
import cv2 

def GetEmptyBoard(cap):
    emptyBoard = None
    print("Press enter when chess board is empty: ")
    while cap.isOpened():
        ret, frame = cap.read()
        key = cv2.waitKey(10) & 0xFF
        cv2.imshow('Raw Webcam Feed', frame)
        if key == 13:  # Enter key
            emptyBoard = frame
            break
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    return emptyBoard

def GetStartingBoard(cap):
    startingBoard = None
    print("Press enter when chess board is setup: ")
    while cap.isOpened():
        ret, frame = cap.read()
        key = cv2.waitKey(10) & 0xFF
        cv2.imshow('Raw Webcam Feed', frame)
        if key == 13:  # Enter key
            startingBoard = frame
            break
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    
    return startingBoard

def GetNextImage(cap, holistic, mp_drawing, mp_holistic):
    while cap.isOpened():
        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)
        # print(results.face_landmarks)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Right hand
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                    mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                                    mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                                    )

        # Left Hand
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                    mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
                                    mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                                    )
        cv2.imshow('Raw Webcam Feed', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

def setupVideo():
    mp_drawing = mp.solutions.drawing_utils
    mp_holistic = mp.solutions.holistic

    mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)
    mp_drawing.draw_landmarks
    cap = cv2.VideoCapture(0)
    holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    return mp_drawing, mp_holistic, cap, holistic

if __name__ == "__main__":
    mp_drawing, mp_holistic, cap, holistic = setupVideo()
    GetNextImage(cap, holistic, mp_drawing, mp_holistic)
    cap.release()
    cv2.destroyAllWindows()