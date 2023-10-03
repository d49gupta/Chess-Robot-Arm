import cv2 as cv
import numpy as np

def resize(img, scale):
    width = int(img.shape[1] * scale / 100)
    height = int(img.shape[0] * scale / 100)
    dim = (width, height)
    resized = cv.resize(img, dim, interpolation=cv.INTER_AREA)

    return resized

class ChessPiece: 
    def __init__(self, color, piece_type, empty = False): #self only used for instances of a class
        self.color = color
        self.piece_type = piece_type
        self.empty = empty

    def __str__(self): #when called, outputs the elements of the chess piece, call by doing str(instance) or instace.__str()
        if self.empty:
            return "Empty"
        return f"{self.color} {self.piece_type}"

def starting_position(board):
    board[0][0] = ChessPiece("W", "r")
    board[1][0] = ChessPiece("W", "h")
    board[2][0] = ChessPiece("W", "b")
    board[3][0] = ChessPiece("W", 'q')
    board[4][0] = ChessPiece("W", "k")
    board[5][0] = ChessPiece("W", "b")
    board[6][0] = ChessPiece("W", "h")
    board[7][0] = ChessPiece("W", "r")

    board[0][7] = ChessPiece("B", "r")
    board[1][7] = ChessPiece("B", "h")
    board[2][7] = ChessPiece("B", "b")
    board[3][7] = ChessPiece("B", 'q')
    board[4][7] = ChessPiece("B", "k")
    board[5][7] = ChessPiece("B", "b")
    board[6][7] = ChessPiece("B", "h")
    board[7][7] = ChessPiece("B", "r") 

    for i in range(8):
        board[i][1] = ChessPiece("W", "p")
        board[i][6] = ChessPiece("B", "p")

if __name__ == "__main__":
    # img = cv.imread(r'C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\Images/chess2.jpg')
    # image = resize(img, 15)
    # canny = cv.Canny(image, 125, 175)

    # rows = 8
    # board = [[0 for x in range(rows)] for y in range(rows)] 
    # starting_position(board)

    # cv.imshow('Original', image)
    # cv.imshow('ROI', canny)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    my_list = [3.7537537537537538, 4.365904365904366, False, False, False, False, 3.6523009495982466, 4.129129129129129, 3.2857142857142856, 4.294871794871795, False, False, False, False, 2.772002772002772, 3.8345864661654137, 6.2406015037593985, 5.128205128205128, False, False, False, False, 3.433162892622352, 4.511278195488721, False, 4.925775978407557, False, False, False, False, 1.7069701280227598, 3.011583011583012, 6.992481203007518, False, False, 5.989773557341125, 4.382761139517896, False, False, 4.015444015444015, 7.181467181467181, 6.0455192034139404, 0.22522522522522523, False, False, False, 2.6234567901234565, 4.761904761904762, 6.122448979591836, 9.18918918918919, False, False, False, False, 5.709876543209877, 5.959183673469388, 8.262548262548263, 5.113221329437546, False, False, 9.30930930930931, False, 2.8528528528528527, 4.16988416988417]

    count_non_false = sum(1 for item in my_list if item is not False)

    print("Number of non-False values:", count_non_false)
