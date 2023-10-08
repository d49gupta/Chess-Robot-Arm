import cv2
import numpy as np
from human_move_recognition import resize


# Read the image
im = cv2.imread(r'C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\4Move_Checkmate\first_move.jpg', cv2.IMREAD_GRAYSCALE)
gray = resize(im, 15)

# Apply thresholding
_, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter out small contours
min_contour_area = 175  # Adjust this threshold as needed
filtered_contours = [contour for contour in contours if cv2.contourArea(contour) > min_contour_area]

# Count the pieces
piece_count = len(filtered_contours)

print("Number of chess pieces:", piece_count)

# Draw contours for visualization (optional)
output_image = gray.copy()
cv2.drawContours(output_image, filtered_contours, -1, (0, 255, 0), 2)

# Display the result (optional)
cv2.imshow("Chessboard", output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()