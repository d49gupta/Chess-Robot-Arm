import cv2
import numpy as np

# Load an image
image = cv2.imread(r"C:\Users\16134\OneDrive - University of Waterloo\Documents\School\Second Year\2B\MTE 203\Project 2\Images\hexagon.png", cv2.IMREAD_GRAYSCALE)

block_size = 2

# Define the aperture parameter for the Sobel operator (typically 3)
ksize = 3

# Define the Harris corner detection parameter (a small value, e.g., 0.04)
k = 0.04

# Apply Harris corner detection
corners = cv2.cornerHarris(image, block_size, ksize, k)

# Threshold value to filter out weak corners
threshold = 0.01 * corners.max()

#Print Stats
num_corners = np.sum(corners > threshold)
print(num_corners)
print(corners)

# Convert to BGR format for color image
corner_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

# Mark the corners on the original image with larger red circles
for y in range(image.shape[0]):
    for x in range(image.shape[1]):
        if corners[y, x] > threshold:
            cv2.circle(corner_image, (x, y), 5, (0, 0, 255), -1)  # Adjust the circle radius (5) for larger markings

# Display the original image with marked corners
cv2.imshow('Harris Corners', corner_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
