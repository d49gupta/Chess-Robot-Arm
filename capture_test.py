import cv2
import numpy as np

from human_move_recognition import resize
from human_move_recognition import line_length
from human_move_recognition import find_interior_corners
from human_move_recognition import find_exterior_corners

def determine_color(square_index):
    # Calculate the row and column of the square
    row = square_index // 8
    col = square_index % 8

    # Determine the color based on the row and column
    if (row % 2 == 0 and col % 2 == 0) or (row % 2 == 1 and col % 2 == 1):
        return 'Black'
    else:
        return 'White'

def grid_search(image, chess_nodes):
    last_valid_node, next_row = 71, 9
    grid_occupied = []
    arr = []
    for i in range(last_valid_node):
        if i % next_row != 8: #cant have last column or last row
            square = image[chess_nodes[i][1]:chess_nodes[i + next_row][1], chess_nodes[i][0]:chess_nodes[i + 1][0]]   
            grey_square = cv2.cvtColor(square, cv2.COLOR_BGR2GRAY)

            # if determine_color(i) == 'Black': # black square
            #     threshold = 60
            # elif determine_color(i) == 'White': # white square
            #     threshold = 135

            threshold = 55
            _, binary_image = cv2.threshold(grey_square, threshold, 255, cv2.THRESH_BINARY)
            # cv2.imshow('Original image', square)
            # cv2.imshow("binary image", binary_image)
            total_pixels = binary_image.size
            white_pixels = np.count_nonzero(binary_image == 255)
            black_pixels = np.count_nonzero(binary_image == 0)

            white_percentage = white_pixels/total_pixels*100
            black_percentage = black_pixels/total_pixels*100

            if white_percentage > black_percentage:
                arr.append('White')
            elif black_percentage > white_percentage:
                arr.append('Black')

            mean_color = np.mean(grey_square, axis=(0, 1))
            grid_occupied.append(mean_color)

    return grid_occupied, arr

def detect_changes(initial_image, current_image):
    # Convert images to grayscale for subtraction
    initial_gray = cv2.cvtColor(initial_image, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)

    # Calculate absolute difference between the two images
    diff = cv2.absdiff(initial_gray, current_gray)

    # Apply threshold to identify regions of significant change
    threshold_value = 30  # Adjust this threshold as needed
    _, thresholded_diff = cv2.threshold(diff, threshold_value, 255, cv2.THRESH_BINARY)

    # Optionally, apply morphological operations to further process the changes
    kernel = np.ones((5, 5), np.uint8)
    thresholded_diff = cv2.morphologyEx(thresholded_diff, cv2.MORPH_OPEN, kernel)

    return thresholded_diff

if __name__ == "__main__":
    img = cv2.imread(r'C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\4Move_Checkmate\emptyBoard.jpg')
    image = resize(img, 15)
    all_nodes = find_exterior_corners(image)

    img = cv2.imread(r'C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\4Move_Checkmate\starting_position.jpg')
    image_start = resize(img, 15)
    grid_occupied1, binary1 = grid_search(image_start, all_nodes)


    img2 = cv2.imread(r'C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\4Move_Checkmate\first_move.jpg')
    image_end = resize(img2, 15)
    grid_occupied2, binary2 = grid_search(image_end, all_nodes)

    thing1 = []
    for i in range(len(grid_occupied1)):
        diff = abs(grid_occupied1[i] - grid_occupied2[i])
        thing1.append(diff)
    average1 = sum(thing1) / len(thing1)

    output_array = [0]*len(thing1)
    sorted_input = sorted(thing1, reverse=True)
    median1 = sorted_input[15]

    # thing2 = []
    # for i in range(len(binary1)):
    #     result = tuple(x - y for x, y in zip(binary1[i], binary2[i])) 
    #     thing2.append(result) #result[0] = -result[1] since percentage has to sum to 100%

    # sum = 0
    # for i in range(len(thing2)):
    #     sum += abs(thing2[i][0])
    # average2 = sum/len(thing2)

    # output_array1 = [0]*len(thing2)
    # sorted_input1 = sorted(thing2, reverse=True)
    # median2 = sorted_input1[9]
    
    # print(thing1)
    # print(thing1[38], thing1[36], average1, median1)
    # print()
    # print(thing2)
    # print(thing2[33], thing2[35], average2, median2) 

    print(binary1)
    print()
    print(binary2)

    print(thing1[33], thing1[35], median1)
        

    cv2.waitKey(0)
    cv2.destroyAllWindows()