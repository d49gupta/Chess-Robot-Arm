import socket
import subprocess
import json

def run_matlab_program():
    matlab_command = f'matlab -batch {"InverseKinematics"}'
    try:
        result = subprocess.run(matlab_command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("MATLAB Output:")
        print(result.stdout)
        if result.returncode == 0:
            print("MATLAB script ran successfully.")
        else:
            print(f"MATLAB script exited with an error (Exit Code {result.returncode}).")
    except subprocess.CalledProcessError as e:
        print(f"Error running MATLAB script: {e}")

def send_message(data_to_send, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))  # Bind to a specific IP address and port
    server_socket.listen(1)  # Listen for incoming connections
    print("Waiting for MATLAB connection...")
    client_socket, client_address = server_socket.accept()  # Accept a client connection

    client_socket.send(data_to_send.encode())
    print("Message sent")

    client_socket.close()
    server_socket.close()

def receive_message(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))  # Bind to a specific IP address and port
    server_socket.listen(1)  # Listen for incoming connections
    print("Waiting for a connection...")
    client_socket, client_address = server_socket.accept()  # Accept a client connection

    data_received = client_socket.recv(1024).decode()
    print("Received message from MATLAB:", data_received)

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    coordinates = {'x': 10, 'y': 10, 'z': 10}
    data_json = json.dumps(coordinates)
    send_message(data_json, 12345)
