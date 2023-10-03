import cv2
import numpy as np
import chess
from chessboard import display
global game_move
# global numb_pieces


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

def determine_color(square_index):
    # Calculate the row and column of the square
    row = square_index // 8
    col = square_index % 8

    # Determine the color based on the row and column
    if (row % 2 == 0 and col % 2 == 0) or (row % 2 == 1 and col % 2 == 1):
        return 'Black'
    else:
        return 'White'

def grid_search(image, canny_image, chess_nodes, numb_pieces):
    last_valid_node, next_row = 71, 9
    grid_canny_occupied = []
    grid_binary_occupied = []

    for i in range(last_valid_node):
        if i % next_row != 8: #cant have last column or last row

            # Canny Array
            square = canny_image[chess_nodes[i][1]:chess_nodes[i + next_row][1], chess_nodes[i][0]:chess_nodes[i + 1][0]] 
            white_canny_pixels = np.count_nonzero(square == 255) 
            total_pixels = square.size 
            white_canny_ratio = (white_canny_pixels / total_pixels) * 100
            grid_canny_occupied.append(white_canny_ratio)

            # Thresholding Array
            binary_square = image[chess_nodes[i][1]:chess_nodes[i + next_row][1], chess_nodes[i][0]:chess_nodes[i + 1][0]]   
            grey_square = cv2.cvtColor(binary_square, cv2.COLOR_BGR2GRAY) 
            if determine_color(i) == 'Black': # black square
                threshold = 65
            elif determine_color(i) == 'White': # white square
                threshold = 185 
            
            _, binary_image = cv2.threshold(grey_square, threshold, 255, cv2.THRESH_BINARY)
            total_pixels = binary_image.size
            white_pixels = np.count_nonzero(binary_image == 255)
            black_pixels = np.count_nonzero(binary_image == 0)
            white_percentage = white_pixels/total_pixels*100
            black_percentage = black_pixels/total_pixels*100
            total = (white_percentage, black_percentage)
            grid_binary_occupied.append(total)


    output_array = [0]*len(grid_canny_occupied)
    sorted_input = sorted(grid_canny_occupied)
    threshold = sorted_input[numb_pieces] # Only keep the highest numbers (# of pieces)
    for i in range(len(grid_canny_occupied)):
        if grid_canny_occupied[i] >= threshold:
            output_array[i] = grid_canny_occupied[i]
        else:
            output_array[i] = 0

    return output_array, grid_binary_occupied

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
    move = "Move Not Found"
    global numb_pieces

    for i in range(len(start_occupied)):
        # No Capture
        if start_occupied[i] > 0 and end_occupied[i] == 0:
            for j in range(len(end_occupied)):
                if end_occupied[j] > 0 and start_occupied[j] == 0:
                    move = map[i] + map[j]

        # Capture
        # Short/Long Castle
        # En Passant
    return move

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
    grid_canny_occupied_start, grid_binary_occupied_start = grid_search(starting_position_roi, result_image, all_nodes, numb_pieces)

    end_position_roi = resize(img_end, 15)
    end_position_canny = cv2.Canny(end_position_roi, 125, 175)
    
    # cv2.imshow(f"Move {game_move}", img_start)
    # cv2.imshow(f"Move {game_move + 1}", img_end)

    result_image_end = line_detector(end_position_roi, end_position_canny)
    grid_occupied_canny_end, grid_binary_occupied_end = grid_search(end_position_roi, result_image_end, all_nodes, numb_pieces)

    game_move = game_move + 1
    move = find_move(grid_canny_occupied_start, grid_occupied_canny_end)
    move_uci = chess.Move.from_uci(move)

    if move_uci in board.legal_moves:
        board.push(move_uci)
        if board.is_check():
            print(print(f"Move {game_move}: {move}, You are in Check!"))
        else:
            print(f"Move {game_move}: {move}")
        print(board)

    return board

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

        board = start_end_moves(move[i], move[i+1], all_nodes, board)

    cv2.waitKey(0)
    cv2.destroyAllWindows()