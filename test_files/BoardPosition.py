import cv2
import numpy as np
import chess
from chessboard import display

def resize(img, scale):
    width = int(img.shape[1] * scale / 100)
    height = int(img.shape[0] * scale / 100)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    return resized

def line_length(x1, y1, x2, y2):
    return abs(np.sqrt((x2 - x1)**2 + (y2 - y1)**2))

def find_interior_corners(input_image):
    gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    rows, cols = 7, 7  # Number of inner corners
    ret, corners = cv2.findChessboardCorners(gray_image, (cols, rows), None)

    if ret:
        cv2.drawChessboardCorners(input_image, (cols, rows), corners, ret) #draws interior corners, stored in corners array
        corners_sorted_x = sorted(corners, key=lambda corner: corner[0][0]) #sort by increasing order of x coordinate

        interior_nodes = [] # sort interior nodes 
        for i in range(rows):
            index = i*rows 
            sorted_elements = sorted(corners_sorted_x[index:index + rows], key=lambda corner: corner[0][1], reverse = True) #sort each column by descending y coordinates
            interior_nodes[index:index + rows] = sorted_elements

        return interior_nodes
    else:
        print("Chessboard corners not found.")

def find_exterior_corners(input_image):
        interior_nodes = find_interior_corners(input_image)
        rows, cols = 7, 7

        x, y = interior_nodes[0][0]
        a, b = interior_nodes[1][0]
        c, d = interior_nodes[rows][0]
        dx = line_length(x, y, a, b)
        dy = line_length(x, y, c, d)

        top_left_interior = min(interior_nodes[:7], key=lambda corner: corner[0][1])
        top_left = (int(top_left_interior[0][0] - dx), int(top_left_interior[0][1] - dy))

        bottom_left_interior = max(interior_nodes[:7], key=lambda corner: corner[0][1])
        bottom_left = (int(bottom_left_interior[0][0] - dx), int(bottom_left_interior[0][1] + dy))

        top_right_interior = min(interior_nodes[42:], key=lambda corner: corner[0][1])
        top_right = (int(top_right_interior[0][0] + dx), int(top_right_interior[0][1] - dy))

        bottom_right_interior = max(interior_nodes[42:], key=lambda corner: corner[0][1])
        bottom_right = (int(bottom_right_interior[0][0] + dx), int(bottom_right_interior[0][1] + dy))

        corners = [bottom_left, top_left, bottom_right, top_right]   

        # Draw Chess Board Corners
        cv2.circle(input_image, (bottom_left[0], bottom_left[1]), 5, (0, 0, 255), -1) 
        cv2.circle(input_image, (top_left[0], top_left[1]), 5, (0, 0, 255), -1) 
        cv2.circle(input_image, (top_right[0], top_right[1]), 5, (0, 0, 255), -1) 
        cv2.circle(input_image, (bottom_right[0], bottom_right[1]), 5, (0, 0, 255), -1) 

        # Chess Board Corners
        chess_nodes = [None]*81
        chess_nodes[0] = top_left
        chess_nodes[8] = top_right
        chess_nodes[72] = bottom_left
        chess_nodes[80] = bottom_right

        counter = 0
        counter_top = 1
        for i in range(len(interior_nodes)):
            x = int(interior_nodes[i][0][0])
            y = int(interior_nodes[i][0][1])

            # Bottom Exterior Side
            if (i % rows == 0):
                counter = counter + 1 #for interior nodes
                a = y + int(dy)
                index = 72 + counter
                chess_nodes[index] = (x, a)
                cv2.circle(input_image, (x, a), 5, (0, 0, 255), -1)
            
            # Left Exterior Side
            if (i < rows):
                a = x - int(dx)
                index = 9*(rows-i)
                chess_nodes[index] = (a, y)
                cv2.circle(input_image, (a, y), 5, (0, 0, 255), -1) 

            # Top Exterior Side
            if (i % rows == 6):
                a = y - int(dy)
                index = counter_top
                counter_top = counter_top + 1
                chess_nodes[index] = (x, a)
                cv2.circle(input_image, (x, a), 5, (0, 0, 255), -1)

            # Right Exterior Side
            if (i >= 42):
                a = x + int(dx)
                index = 9*(8 - (i % rows)) - 1
                chess_nodes[index] = (a, y)
                cv2.circle(input_image, (a, y), 5, (0, 0, 255), -1)

            index = 9*(rows-(i%rows)) + counter
            chess_nodes[index] = (x, y) # fills all interior nodes
            cv2.circle(input_image, (x, y), 5, (0, 0, 255), -1) 

        return interior_nodes, corners, chess_nodes

def find_roi(crop, corners):

    # cv2.line(draw, corners[1], corners[3], (255, 0, 0), 1)
    # cv2.line(draw, corners[1], corners[0], (255, 0, 0), 1)
    # cv2.line(draw, corners[3], corners[2], (255, 0, 0), 1)
    # cv2.line(draw, corners[0], corners[2], (255, 0, 0), 1)

    roi = crop[int(corners[3][1]):int(corners[0][1]), int(corners[1][0]):int(corners[2][0])]

    # slanted_square = np.array([[corners[0][0], corners[0][1]], [corners[1][0], corners[1][1]], [corners[2][0], corners[2][1]], [corners[3][0], corners[2][1]]], dtype=np.float32)
    # regular_square = np.array([[0, 0], [image.shape[1], 0], [image.shape[1], image.shape[0]], [0, image.shape[0]]], dtype=np.float32)
    # matrix = cv2.getPerspectiveTransform(slanted_square, regular_square)
    # output_square = cv2.warpPerspective(image, matrix, (image.shape[0], image.shape[1]))  # Adjust the size as needed
    # roi = output_square[0:image.shape[0], 0:image.shape[1]]
    return roi

def hough_line_transform(starting_position_canny, image):
    lines = cv2.HoughLinesP(starting_position_canny, rho=1, theta=np.pi / 180, threshold=50, minLineLength=50, maxLineGap=5)

    # Draw detected lines 
    if lines is not None:
        for line in lines:
            if len(line[0]) == 4:  # Check if line has exactly four values (x1, y1, x2, y2)
                x1, y1, x2, y2 = line[0]
                cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
    
    return lines

def line_detector(image, canny_image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    lsd = cv2.createLineSegmentDetector(0)
    lines, width, prec, nfa = lsd.detect(gray)

    image_height, image_width, image_channels = image.shape
    output_image = np.zeros((image_height, image_width, 3), dtype=np.uint8)

    # Draw the detected lines on the output image
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = map(int, line[0])
            cv2.line(output_image, (x1, y1), (x2, y2), (255, 255, 255), 2)
    # cv2.imshow('Image with Detected Lines', output_image)

    result_image = np.zeros_like(canny_image) # Black image
    for i in range(canny_image.shape[0]):
        for j in range(canny_image.shape[1]):
            if np.all(output_image[i, j] == 0):  # Check if all elements in the pixel are zero
                result_image[i, j] = canny_image[i, j]    

    return result_image

def grid_search(canny_image, chess_nodes):
    last_valid_node, next_row = 71, 9
    # threshold = 2.75
    grid_occupied = []
    for i in range(last_valid_node):
        if i % next_row != 8: #cant have last column or last row
            square = canny_image[chess_nodes[i][1]:chess_nodes[i + next_row][1], chess_nodes[i][0]:chess_nodes[i + 1][0]]   
            white_pixels = np.count_nonzero(square == 255) 
            total_pixels = square.size 
            white_ratio = (white_pixels / total_pixels) * 100
            grid_occupied.append(white_ratio)
            # if white_ratio >= threshold:
            #     grid_occupied.append(white_ratio)
            # else:
            #     grid_occupied.append(False)
    
    output_array = [0]*len(grid_occupied)
    sorted_input = sorted(grid_occupied)

    mean = sum(sorted_input) / len(sorted_input) 
    median = sorted_input[32] # Only keep the highest numbers (# of pieces)

    # print(mean)
    # print(median)
    # print(sorted_input[31])

    for i in range(len(grid_occupied)):
        if grid_occupied[i] >= median:
            output_array[i] = grid_occupied[i]
        else:
            output_array[i] = 0

    return output_array

def create_map():
    chessboard_size = 8
    index_to_chess_position = []

    for row in range(chessboard_size):
        for col in range(chessboard_size):
            chess_position = chr(ord('a') + row) + str(col + 1) # Convert row and column to chess notation (a1, a2, b1, etc.)
            index_to_chess_position.append(chess_position)

    return index_to_chess_position

def find_move(start_occupied, end_occupied):
    map = create_map()
    move = "Not Found"

    for i in range(len(start_occupied)):
        if start_occupied[i] > 0 and end_occupied[i] == 0:
            for j in range(len(end_occupied)):
                if end_occupied[j] > 0 and start_occupied[j] == 0:
                    move = map[i] + map[j]
    return move

if __name__ == "__main__":
    img = cv2.imread(r'C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\4Move_Checkmate\emptyBoard.jpg')
    empty_board_roi = resize(img, 15) #original image (resized) for ROI
    empty_board_draw = resize(img, 15) #new image to draw on

    interior_nodes, corners, all_nodes = find_exterior_corners(empty_board_draw)
    empty_roi = find_roi( empty_board_roi, corners) #draws on input_image, crops board on image
    
    # cv2.imshow('Empty Board w Corners', empty_board_draw)
    # # cv2.imshow('Empty board ROI', empty_roi)

    img_start = cv2.imread(r'C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\4Move_Checkmate\fourth_move.jpg')
    starting_position_draw = resize(img_start, 15)
    starting_position_roi = resize(img_start, 15)
    starting_position_canny = cv2.Canny(starting_position_roi, 125, 175)

    # full_roi = find_roi(starting_position_draw, starting_position_roi, corners)
    # starting_position_canny_roi = cv2.Canny(full_roi, 125, 175)  

    # cv2.imshow('Starting Position Draw', starting_position_draw)
    # cv2.imshow('Starting Position ROI & Canny', starting_position_canny)

    result_image = line_detector(starting_position_roi, starting_position_canny)
    # cv2.imshow('Filtered Lines lol', result_image)

    grid_occupied = grid_search(result_image, all_nodes)
    # print(grid_occupied)

    img_end = cv2.imread(r'C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\4Move_Checkmate\fifth_move.jpg')
    starting_position_draw_end = resize(img_end, 15)
    starting_position_roi_end = resize(img_end, 15)
    starting_position_canny_end = cv2.Canny(starting_position_roi_end, 125, 175)

    # cv2.imshow('End Position Draw', starting_position_draw_end)
    result_image_end = line_detector(starting_position_roi_end, starting_position_canny_end)
    final_filter = find_roi(result_image_end, corners)
    cv2.imshow('Filtered Lines lol', final_filter)
    grid_occupied_end = grid_search(result_image_end, all_nodes)
    # print(grid_occupied_end)

    move = find_move(grid_occupied, grid_occupied_end)
    print(move)

    cv2.waitKey(0)
    cv2.destroyAllWindows()