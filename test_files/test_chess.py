import chess
from chessboard import display

# Initialize pygame
display.pygame.init()

# Create a chessboard
board = chess.Board()
valid_fen = board.fen()  # Get the initial FEN string
game_board = display.start(fen=valid_fen)  # Initialize the GUI chessboard with the FEN starting string

running = True
while running:
    for event in display.pygame.event.get():  # Check for QUIT event (e.g., closing the window)
        if event.type == display.pygame.QUIT:
            running = False
    
    # Make a move in the chess game 
    move = "b1c3" # Start, end position
    if chess.Move.from_uci(move) in board.legal_moves: #chech if legal move
        board.push_uci(move)
        valid_fen = board.fen() # Get updated FENs
        display.update(valid_fen, game_board) # Update GUI with new move
    else:
        print("Invalid move. Try again.")

display.terminate()

# def make_move(board, game_board, move, running):
#     for event in display.pygame.event.get():  # Check for QUIT event (e.g., closing the window)
#         if event.type == display.pygame.QUIT:
#             running = False
#             return running
    
#     # Make a move in the chess game 
#     # move = "b1c3" # Start, end position
#     if chess.Move.from_uci(move) in board.legal_moves: #chech if legal move
#         board.push_uci(move)
#         valid_fen = board.fen() # Get updated FENs
#         display.update(valid_fen, game_board) # Update GUI with new move
#     else:
#         print("Invalid move. Try again.")

# if __name__ == "__main__":
#     board = chess.Board()
#     valid_fen = board.fen()  # Get the initial FEN string
#     game_board = display.start(fen=valid_fen)  # Initialize the GUI chessboard with the FEN starting string

#     running = True
#     while running:
#         move = input("b1c3")
#         running = make_move(board, game_board, move, running)
    
#     display.terminate