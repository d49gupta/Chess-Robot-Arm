import cv2
import numpy as np 

def resize(img, scale):
    width = int(img.shape[1] * scale / 100)
    height = int(img.shape[0] * scale / 100)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    return resized

def filter(image):
    blurred1 = cv2.medianBlur(image, 5)
    blurred = cv2.GaussianBlur(blurred1, (9, 9), 2)

    thresh, binary_image = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY) #Set threshold values
    canny = cv2.Canny(binary_image, 125, 175)

    return canny

def line_length(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def filter_corners(corner_image):
    corner_points = np.argwhere(corner_image == (0, 0, 255)) #list of detected corners
    avg_x = int(np.mean([corner[1] for corner in corner_points])) 
    avg_y = int(np.mean([corner[0] for corner in corner_points]))
    cv2.circle(corner_image, (avg_x, avg_y), 2, (0, 255, 0), -1) #midpoint of chess board

    return avg_x, avg_y

def Harris_corner(image, threshold_dist):
    corners = cv2.cornerHarris(image, 2, 3, 0.04) #returns matrix of how likely pixel is corner

    # Threshold value to filter out weak corners
    threshold = 0.01 * corners.max() #only save strong potential corners

    # Convert to BGR format for color image
    corner_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    circle_coordinates = []
    avg_x, avg_y = filter_corners(corner_image)
    # Mark the corners on the original image with larger red circles
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if corners[y, x] > threshold:
                if abs(avg_x - x) <= threshold_dist and abs(avg_y - y) <= threshold_dist:
                    if not np.all(corner_image[y, x] == [0, 0, 255]): # ensures only one corner per pixel
                        cv2.circle(corner_image, (x, y), 2, (0, 0, 255), -1) 
                        circle_coordinates.append((x, y)) #store tuple of circle coordinates 

    return corner_image, circle_coordinates

if __name__ == "__main__":
    img = cv2.imread(r'C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\Images/chess3.jpg', cv2.IMREAD_GRAYSCALE)
    
    image = resize(img, 15)
    canny = filter(image)
    corner_image, circle_coordinates = Harris_corner(canny, 150) #threshold_dist 

    cv2.imshow('Original Image', image)
    cv2.imshow('Harris Corners', corner_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()