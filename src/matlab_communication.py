import socket
import subprocess
import json
import ast

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

def start_server(host, port):
    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    server_address = (host, port)
    server_socket.bind(server_address)
    server_socket.listen(1)
    print('Server listening on {}: {}'.format(*server_address))
    print('Server listening on {}: {}'.format(*server_address))

    # Accept a connection
    client_socket, client_address = server_socket.accept()
    print('Accepted connection from {}:{}'.format(*client_address))

    return server_socket, client_socket

def receive_message(client_socket):
    data_received = client_socket.recv(1024).decode('utf-8')
    print("Received message from MATLAB:")
    # joint_angles = ast.literal_eval(data_received)

    return data_received

def send_message(client_socket, message):
    client_socket.sendall(message.encode())
    print('Sent message to client:')