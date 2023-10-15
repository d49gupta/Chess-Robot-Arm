import cv2

# Create a VideoCapture object to access the webcam (change the device index if needed)
cap = cv2.VideoCapture(1)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Display the frame
    cv2.imshow('Webcam Feed', frame)

    # Check if the Enter key is pressed
    key = cv2.waitKey(1)
    if key == 13:  # 13 is the ASCII code for the Enter key
        # Save the captured frame as an image
        cv2.imwrite('captured_image.jpg', frame)
        print("Image captured!")

    # Press 'q' to quit the loop and close the webcam feed
    if key == ord('q'):
        break

# Release the VideoCapture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()