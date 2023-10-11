import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('localhost', 12345)  # Change host and port to match the server
client_socket.connect(server_address)

# Send data to the server
message = "Hello, Server!"
client_socket.send(message.encode('utf-8'))

# Clean up
client_socket.close()
