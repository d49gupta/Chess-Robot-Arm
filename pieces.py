import cv2
import numpy as np
import chess
from chessboard import display
import sys
global game_move
global numb_pieces


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
    rows, cols = 7, 7  
    ret, corners = cv2.findChessboardCorners(gray_image, (cols, rows), None)

    if ret:
        cv2.drawChessboardCorners(input_image, (cols, rows), corners, ret) 
        corners_sorted_x = sorted(corners, key=lambda corner: corner[0][0]) 

        interior_nodes = [] 
        for i in range(rows):
            index = i*rows 
            sorted_elements = sorted(corners_sorted_x[index:index + rows], key=lambda corner: corner[0][1], reverse = True) 
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

        return chess_nodes

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


def grid_search(image, canny_image, chess_nodes, numb_pieces):
    last_valid_node, next_row = 71, 9
    grid_occupied = []
    mean_occupied = []
    grid_binary_occupied = []

    for i in range(last_valid_node):
        if i % next_row != 8: #cant have last column or last row

            # Canny Array
            square = canny_image[chess_nodes[i][1]:chess_nodes[i + next_row][1], chess_nodes[i][0]:chess_nodes[i + 1][0]]   
            white_pixels = np.count_nonzero(square == 255) 
            total_pixels = square.size 
            white_ratio = (white_pixels / total_pixels) * 100
            grid_occupied.append(white_ratio)

            # Thresholding Array
            binary_square = image[chess_nodes[i][1]:chess_nodes[i + next_row][1], chess_nodes[i][0]:chess_nodes[i + 1][0]]   
            grey_square = cv2.cvtColor(binary_square, cv2.COLOR_BGR2GRAY) 
            if determine_color(i) == 'Black': # black square
                threshold = 65
            elif determine_color(i) == 'White': # white square
                threshold = 185 
            
            _, binary_image = cv2.threshold(grey_square, threshold, 255, cv2.THRESH_BINARY)
            total_binary_pixels = binary_image.size
            white_pixels = np.count_nonzero(binary_image == 255)
            black_pixels = np.count_nonzero(binary_image == 0)
            white_percentage = white_pixels/total_binary_pixels*100
            black_percentage = black_pixels/total_binary_pixels*100

            if white_percentage >= black_percentage:
                grid_binary_occupied.append('White')
            elif black_percentage > white_percentage:
                grid_binary_occupied.append('Black')

            # Mean array
            mean_color = np.mean(grey_square, axis=(0, 1))
            mean_occupied.append(mean_color)
            

    output_array = [0]*len(grid_occupied)
    sorted_input = sorted(grid_occupied)

    threshold = sorted_input[numb_pieces] # Only keep the highest numbers (# of pieces)
    for i in range(len(grid_occupied)):
        if grid_occupied[i] >= threshold:
            output_array[i] = grid_occupied[i]
        else:
            output_array[i] = 0

    return output_array, mean_occupied, grid_binary_occupied

def determine_color(square_index):
    # Calculate the row and column of the square
    row = square_index // 8
    col = square_index % 8

    # Determine the color based on the row and column
    if (row % 2 == 0 and col % 2 == 0) or (row % 2 == 1 and col % 2 == 1):
        return 'Black'
    else:
        return 'White'

def determineBoardPosition(mean_start, mean_end):
    mean_arr = []
    for i in range(len(mean_start)):
        diff = abs(mean_start[i] - mean_end[i])
        mean_arr.append(diff)

    sorted_mean = sorted(mean_arr, reverse=True)
    median_mean = sorted_mean[15]

    # binary_arr = []
    # for i in range(len(binary_start)):
    #     result = tuple(x - y for x, y in zip(binary_start[i], binary_end[i])) 
    #     binary_arr.append(result) #result[0] = -result[1] since percentage has to sum to 100%

    # binary_sum = 0
    # for i in range(len(binary_arr)):
    #     binary_sum += abs(binary_arr[i][0])
    # average_binary = binary_sum/len(binary_arr)

    return mean_arr, median_mean

def create_map():
    chessboard_size = 8
    index_to_chess_position = {}

    for row in range(chessboard_size):
        for col in range(chessboard_size):
            chess_position = chr(ord('a') + row) + str(col + 1)  # Convert row and column to chess notation (a1, a2, b1, etc.)
            index_to_chess_position[len(index_to_chess_position)] = chess_position

    return index_to_chess_position

def find_key_by_value(dictionary, target_value):
    for key, value in dictionary.items():
        if value == target_value:
            return key
    return None  

def find_valid_moves(start_canny, end_canny, mean_diff, mean_median, board):
    map = create_map()
    current_valid_moves = []
    all_valid_moves = list(board.legal_moves)

    for i in range(len(start_canny)):
        if start_canny[i] > 0 and end_canny[i] == 0 and mean_diff[i] > mean_median:
            start_move = map[i]

            for j in range(len(map)):
                if map[j] != start_move:
                    potential_move = start_move + map[j]
                    move_uci = chess.Move.from_uci(potential_move)

                    if move_uci in all_valid_moves:
                        valid_move = (start_move, map[j])
                        current_valid_moves.append(valid_move)

    return start_move, current_valid_moves

def determine_capture(binary_start, binary_end, board, chess_map):

    binary_changes = []
    for i in range(len(binary_start)):
        current_square = chess_map[i]
        square_to_check = chess.parse_square(current_square)
        piece_at_square = board.piece_at(square_to_check)
        
        if piece_at_square is not None:
            if binary_start[i][0] != binary_end[i][0]:
                binary_changes.append(i)
            
    return binary_changes

def find_move(start_canny, end_canny, binary_start, binary_end, valid_moves, board, start_move, numb_pieces):
    chess_map = create_map()
    detected_move = ""
    capture = False

    # Capture
    binary_changes = determine_capture(binary_start, binary_end, board, chess_map)
    if len(binary_changes) > 0: 
        for i in range(len(binary_changes)):
            potential_move = start_move + chess_map[i]
            potential_move_uci = chess.Move.from_uci(potential_move)
            for j in valid_moves:
                if j == potential_move_uci:
                    capture = True
                    detected_move = potential_move
                    numb_pieces =- 1

    # Normal Move
    if capture == False:
        for i in valid_moves:
            chess_index_start = find_key_by_value(chess_map, i[0])
            chess_index_end = find_key_by_value(chess_map, i[1])

            if end_canny[chess_index_end] > 0 and start_canny[chess_index_end] == 0: 
                detected_move = i[0] + i[1]

    if detected_move != '':
        detected_move_uci = chess.Move.from_uci(detected_move)
        board.push(detected_move_uci)
    else:
        print("Move not Found")
        sys.exit()

    return detected_move, numb_pieces

def calibration():
    img_empty = cv2.imread(r'C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\4Move_Checkmate\emptyBoard.jpg')
    empty_board_roi = resize(img_empty, 15) 
    empty_board_draw = resize(img_empty, 15) 
    all_nodes = find_exterior_corners(empty_board_draw)
    game_move = 0
    numb_pieces = 32

    board = chess.Board()
    print(f"Move {game_move}: Starting Position")
    print(board)

    return all_nodes, board, game_move, numb_pieces

def start_end_moves(img_start, img_end, all_nodes, board):
    global game_move
    global numb_pieces

    starting_position_roi = resize(img_start, 15)
    starting_position_canny = cv2.Canny(starting_position_roi, 125, 175)
    result_image = line_detector(starting_position_roi, starting_position_canny)
    grid_occupied_start, mean_start, binary_start  = grid_search(starting_position_roi, result_image, all_nodes, numb_pieces)

    end_position_roi = resize(img_end, 15)
    end_position_canny = cv2.Canny(end_position_roi, 125, 175)
    result_image_end = line_detector(end_position_roi, end_position_canny)
    grid_occupied_end, mean_end, binary_end = grid_search(end_position_roi, result_image_end, all_nodes, numb_pieces)

    mean_arr, mean_median = determineBoardPosition(mean_start, mean_end)

    game_move = game_move + 1
    start_move, valid_moves = find_valid_moves(grid_occupied_start, grid_occupied_end, mean_arr, mean_median, board)
    detected_move, numb_pieces = find_move(grid_occupied_start, grid_occupied_end, binary_start, binary_end, valid_moves, board, start_move, numb_pieces)
    
    return detected_move, board

if __name__ == "__main__":
    all_nodes, board, game_move, numb_pieces = calibration()

    move0 = cv2.imread(r'C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\4Move_Checkmate\starting_position.jpg')
    move1 = cv2.imread(r'C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\4Move_Checkmate\first_move.jpg')
    move2 = cv2.imread(r'C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\4Move_Checkmate\second_move.jpg')
    move3 = cv2.imread(r'C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\4Move_Checkmate\third_move.jpg')
    move4 = cv2.imread(r'C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\4Move_Checkmate\fourth_move.jpg')
    move5 = cv2.imread(r'C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\4Move_Checkmate\fifth_move.jpg')
    move6 = cv2.imread(r'C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\4Move_Checkmate\sixth_move.jpg')

    move = []
    move.append(move0)
    move.append(move1)
    move.append(move2)
    move.append(move3)
    move.append(move4)
    move.append(move5)
    move.append(move6)

    for i in range(len(move) - 1):
        if board.is_checkmate() == True:
            if game_move % 2 == 1:
                print("Black Wins!")
            if game_move % 2 == 0:
                print("White Wins!")
            break

        if board.is_stalemate() == True:
            print("The Game is a Stalemate!")
            break

        if board.is_fivefold_repetition() == True or board.is_seventyfive_moves() == True:
            print("The Game is a Draw!")
            break
        
        detected_move, board = start_end_moves(move[i], move[i+1], all_nodes, board)
        
        print("---------------------------------------------------------------")
        if board.is_check():
            print(print(f"Move {game_move}: {detected_move}, You are in Check!"))
        else:
            print(f"Move {game_move}: {detected_move}")
        print(board)

    cv2.waitKey(0)
    cv2.destroyAllWindows()