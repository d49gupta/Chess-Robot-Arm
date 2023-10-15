import socket
import chess
import json
import sys

def exit_program():
    global server_socket
    if server_socket:
        server_socket.close()
    sys.exit("Program B has been terminated.")

def socket_server(skill_level):
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)  # Change host and port as needed

    try:
        server_socket.bind(server_address)
        server_socket.listen(5)
        print("Server B is  waiting for a connection...")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}")

            try:
                data = client_socket.recv(1024).decode('utf-8')
                print(f"Received info from Program A")
                data = json.loads(data)  # Parse the received JSON data

                engine_move = data['engine_move']
                updated_board = data['fen_str']
                board = updated_board.set_fen()
                print("Chess Engine Move is: ", engine_move)
                print(board)
                
                fen_str, next_move = run_main(board)
                response = {'fen_str': fen_str, 'skill_level': skill_level, 'human_move': next_move}
                response_json = json.dumps(response)

                client_socket.send(response_json.encode('utf-8'))

            except Exception as e:
                print(f"Error while processing data: {e}")
            finally:
                client_socket.close()

    except Exception as e:
        print(f"Server error: {e}")
    finally:
        exit_program()

def run_main(updated_board):
    next_move = input("Enter your first move: ")
    updated_board.push(next_move)
    fen_str = updated_board.fen()

    return fen_str, next_move


def send_message(message):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    server_address = ('localhost', 12345)  # Change host and port to match the server
    client_socket.connect(server_address)

    client_socket.send(message.encode('utf-8'))
    client_socket.close()

if __name__ == "__main__":
    board = chess.Board()
    board.set_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")  # Set the initial position
    starting_fen = board.fen()
    skill_level = int(input("Enter the skill level (1-20, where 1 is the easiest and 20 is the strongest): "))
    initial_move = input("Enter your first move: ")
    board.push_uci(initial_move)
    fen_str = board.fen()

    data = {'fen_str': fen_str, 'skill_level': skill_level, 'human_move': initial_move}
    data_json = json.dumps(data)
    send_message(data_json)
    
    try:
        socket_server(skill_level)
    except KeyboardInterrupt:
        exit_program()