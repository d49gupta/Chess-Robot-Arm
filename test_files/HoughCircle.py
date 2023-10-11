import cv2
import numpy as np

# Load an image
img = cv2.imread(r'C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\Images/chess2.jpg', cv2.IMREAD_COLOR)

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Resize the grayscale image
width = int(gray.shape[1] * 20 / 100)
height = int(gray.shape[0] * 20 / 100)
dim = (width, height)
resized = cv2.resize(gray, dim, interpolation=cv2.INTER_AREA)

# Apply thresholding to the grayscale image
thresh, binary_image = cv2.threshold(resized, 200, 255, cv2.THRESH_BINARY)

# Use Hough Circle Transform to detect circles
circles = cv2.HoughCircles(binary_image, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=0, maxRadius=0)

if circles is not None:
    circles = np.uint16(np.around(circles))
    
    for circle in circles[0, :]:
        center = (circle[0], circle[1])  # Circle center coordinates
        radius = circle[2]  # Circle radius
        
        # Calculate diameter (twice the radius)
        diameter = 2 * radius
        
        # Set a minimum diameter threshold (adjust as needed)
        min_diameter_threshold = 40  # Example threshold (pixels)
        
        if diameter >= min_diameter_threshold:
            cv2.circle(resized, center, radius, (0, 255, 0), 2)  # Draw the circle

# Display the image with detected circles
cv2.imshow('Detected Circles', resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
