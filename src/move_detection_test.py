import unittest
import cv2
import chess_move_detection

class TestMyFunctions(unittest.TestCase):

    def test_white_squares(self):
        a8 = chess_move_detection.determine_color(7)
        b1 = chess_move_detection.determine_color(8)
        self.assertEqual(a8, 'White')
        self.assertEqual(b1, 'White')

    def test_black_squares(self):
        a1 = chess_move_detection.determine_color(0)
        c1 = chess_move_detection.determine_color(16)
        self.assertEqual(a1, 'Black')
        self.assertEqual(c1, 'Black')

    def test_map(self):
        chess_map = chess_move_detection.create_map()
        a1 = chess_move_detection.find_key_by_value(chess_map, 'a1')
        b8 = chess_move_detection.find_key_by_value(chess_map, 'b8')
        h6 = chess_move_detection.find_key_by_value(chess_map, 'h6')
        e2 = chess_move_detection.find_key_by_value(chess_map, 'e2')

        self.assertEqual(a1, 0)
        self.assertEqual(b8, 15)
        self.assertEqual(h6, 61)
        self.assertEqual(e2, 33)

    def test_normal_move(self):
        calibration_image = cv2.imread(r'C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\4Move_Checkmate\emptyBoard.jpg')
        start_move = cv2.imread(r'C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\4Move_Checkmate\starting_position.jpg')
        first_move = cv2.imread(r'C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\4Move_Checkmate\first_move.jpg')

        all_nodes, board, game_move, numb_pieces = chess_move_detection.calibration(calibration_image)
        detected_move, board, game_move = chess_move_detection.start_end_moves(start_move, first_move, all_nodes, board, numb_pieces, game_move)
        self.assertEqual(detected_move, 'e2e4')

    def test_capture_move(self):
        calibration_image = cv2.imread(r'C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\capture_test_images\empty_board.jpg')
        second_move = cv2.imread(r'C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\capture_test_images\move2.jpg')
        third_move = cv2.imread(r'C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\capture_test_images\move3.jpg')

        all_nodes, board, game_move, numb_pieces = chess_move_detection.calibration(calibration_image)
        detected_move, board, game_move = chess_move_detection.start_end_moves(second_move, third_move, all_nodes, board, numb_pieces, game_move)
        self.assertEqual(detected_move, 'e4d5')


if __name__ == '__main__':
    unittest.main() 
