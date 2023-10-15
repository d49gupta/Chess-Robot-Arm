import socket
import chess
import json
import sys
from stockfish import Stockfish

def exit_program():
    global server_socket
    if server_socket:
        server_socket.close()
    sys.exit("Program A has been terminated.")

def socket_server():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)  # Change host and port as needed

    try:
        server_socket.bind(server_address)
        server_socket.listen(5)
        print("Server A is waiting for a connection...")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}")

            try:
                data = client_socket.recv(1024).decode('utf-8')
                print(f"Received info from Program A")
                data = json.loads(data)  # Parse the received JSON data
                opponent_move = data['human_move']
                skill_level = data['skill_level']
                fen_str = data['fen_str']
                updated_board = chess.Board(fen_str)  # Create a board from the FEN string

                response = run_main(opponent_move, skill_level, updated_board)
                client_socket.send(response.encode('utf-8'))

            except Exception as e:
                print(f"Error while processing data: {e}")
            finally:
                client_socket.close()

    except Exception as e:
        print(f"Server error: {e}")
    finally:
        exit_program()

def run_main(opponent_move, skill_level, board):
    stockfish = Stockfish("path/to/stockfish/executable")  # Replace with the correct path
    stockfish.set_skill_level(skill_level)

    try:
        move = chess.Move.from_uci(opponent_move)
        if move in board.legal_moves:
            stockfish.position(board)
            best_move_uci = stockfish.get_best_move()
            best_move = chess.Move.from_uci(best_move_uci)
            board.push(best_move)
            fen_str = board.fen()

            data = {
                'engine_move': best_move_uci,
                'fen_str': fen_str
            }
            data_json = json.dumps(data)

            return data_json
        else:
            print("Invalid Move")
            exit_program()

    except Exception as e:
        print(f"Error in run_main: {e}")
        return None
    
    except KeyboardInterrupt:
        exit_program()


if __name__ == "__main__":
    try:
        socket_server()
    except KeyboardInterrupt:
        exit_program()
