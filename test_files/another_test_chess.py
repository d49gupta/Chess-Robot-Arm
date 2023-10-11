# import chess
# from chessboard import display

# # Create a chessboard
# board = chess.Board()
# valid_fen = board.fen()  # Get the initial FEN string
# game_board = display.start(fen=valid_fen)  # Initialize the GUI chessboard with the FEN starting string

# while True:
#     display.check_for_quit()
    
#     move = input("Enter a move (in SAN notation): ")
#     if (chess.move in board.legal_moves):
#         board.push_san(move)
#         valid_fen = board.fen()
#         display.update(valid_fen, game_board)

#     # board flip interface
#     if not game_board.flipped:
#         display.flip(game_board)

import chess

# Create an empty chess board
board = chess.Board()

# Access the piece on e2

piece = board.piece_at(chess.D8)

# Print information about the piece
print(piece)  # This will output "P" to represent a white pawn
print(piece.color)  # This will output "True" to represent a white piece
print(piece.symbol())  # This will output "P" to represent a pawn
