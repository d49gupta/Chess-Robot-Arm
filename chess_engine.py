from stockfish import Stockfish

stockfish = Stockfish(r"C:\Users\16134\OneDrive\Documents\Learning\Hardware\Raspberry Pi\Chess Robot Arm\stockfish-windows-x86-64-modern\stockfish\stockfish-windows-x86-64-modern.exe")

# Get the user's desired skill level
while True:
    try:
        skill_level = int(input("Enter the skill level (1-20, where 1 is the easiest and 20 is the strongest): "))
        if 1 <= skill_level <= 20:
            break
        else:
            print("Invalid skill level. Please enter a number between 1 and 20.")
    except ValueError:
        print("Invalid input. Please enter a valid number between 1 and 20.")
stockfish.set_skill_level(skill_level)

# Starting Position
initial_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
stockfish.set_fen_position(initial_fen)

while True:
    opponent_move = input("Enter opponent's move (in UCI format): ")

    if stockfish.is_move_correct(opponent_move):
        stockfish.make_moves_from_current_position([opponent_move])
        best_move = stockfish.get_best_move()
        print(f"Stockfish's move: {best_move}")
        stockfish.make_moves_from_current_position([best_move])
    else:
        print("Invalid move, try again!")