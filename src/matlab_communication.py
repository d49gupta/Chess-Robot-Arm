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
    server_socket.bind(server_address)
    server_socket.listen(1)
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

if __name__ == "__main__":
    server_socket, client_socket = start_server(12399)
    coordinates_list = ["-135.0000, -130.4900, -143.6109,  113.7369,  -45.0003", "-135.0000, -130.4900, -143.6109,  113.7369,  -45.0003"]

    for coordinates in coordinates_list:
        send_message(client_socket, coordinates)
        joint_angles = receive_message(client_socket)

        # for i in range(len(joint_angles)):
        #     if joint_angles[i] < 0:
        #         joint_angles[i] += 180
        #     print("Joint Angle %d: %f" % (i + 1, joint_angles[i]))

    send_message(client_socket, 'exit')

    client_socket.close()
    server_socket.close()
