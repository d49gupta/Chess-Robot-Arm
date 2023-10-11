import socket
import sys

# Define a global variable to store the server socket
server_socket = None

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
                print(f"Received from Program B: {data}")
                response = run_main(data)
                client_socket.send(response.encode('utf-8'))

            except Exception as e:
                print(f"Error while processing data: {e}")
            finally:
                client_socket.close()
                
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        exit_program()

def run_main(data):
    return f"Program A processed: {data}"

if __name__ == "__main__":
    try:
        socket_server()
    except KeyboardInterrupt:
        exit_program()
