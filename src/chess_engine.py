import chess
import json

def stockfish_make_move(stockfish, skill_level, board, opponent_move, game_move):

    stockfish.set_skill_level(skill_level)
    try:
        if board.is_valid() and chess.Move.from_uci(opponent_move) in board.legal_moves:
            board.push(chess.Move.from_uci(opponent_move))

            stockfish.position(board)
            best_move = stockfish.go(depth=20).bestmove
            board.push(best_move)
            game_move += 1

            return best_move.uci(), board.uci(), game_move
        
    except Exception as e:
        print(f"Error in stockfish_make_move: {e}")
        return None, board.uci()
    
def create_coordinate_dict():
    column_dict = {
        'a': -13, 
        'b': -8.5, 
        'c': -5,
        'd': -1.5, 
        'e': 2,
        'f': 5.5, 
        'g': 9, 
        'h': 12.5
    }
    piece_dict = {
        'p': 5,
        'b': 8,
        'k': 7,
        'r': 6,
        'n': 6,
        'q': 10,
        'k': 12 
    }
    return column_dict, piece_dict

def find_coordinates(move, board):
    string_midpoint = len(move) // 2
    start_move = move[:string_midpoint]
    end_move = move[string_midpoint:]
    file, rank = chess.square_file(chess.SQUARE_NAMES.index(end_move)), chess.square_rank(chess.SQUARE_NAMES.index(end_move))
    current_piece = str(board.piece_at(chess.square(file, rank)).symbol())
    column_dict, piece_dict = create_coordinate_dict()

    moves = [start_move, end_move]
    coordinates_list = []
    for i in moves:
        coordinates = {'x': column_dict[i[0]], 'y': 10 + int(i[1])*2.5, 'z': piece_dict[current_piece.lower()]}
        data_json = json.dumps(coordinates)
        coordinates_list.append(data_json)

    return coordinates_list