import socket
import sys

def connect_to_server(server_address, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, server_port))
    return client_socket

def ftp_client(server_address, server_port):
    client_socket = connect_to_server(server_address, server_port)
    print("Connected to server.")

    try:
        while True:
            command = input("Enter command: ")
            client_socket.send(command.encode())

            if command.startswith("LIST"):
                response = client_socket.recv(4096).decode()
                print(response)
            elif command.startswith("RETRIEVE"):
                file_info = client_socket.recv(1024).decode()
                if ':' in file_info:
                    file_size = int(file_info.split(':')[0])
                    if file_size == 0:
                        print("File not found.")
                        continue
                    filename = command.split()[1]
                    data = file_info.split(':', 1)[1].encode()
                    while len(data) < file_size:
                        data += client_socket.recv(1024)
                    with open(filename, 'wb') as f:
                        f.write(data)
                    print(f"File '{filename}' retrieved successfully.")
            elif command.startswith("STORE"):
                filename = command.split()[1]
                try:
                    with open(filename, 'rb') as file:
                        file_data = file.read()
                    # Send command with filename 
                    client_socket.send(f"STORE {filename}".encode())
                    ack = client_socket.recv(1024).decode()
                    if ack == "READY":
                        client_socket.sendall(file_data)
                        client_socket.shutdown(socket.SHUT_WR) # disable further sends
                        print(f"File '{filename}' stored successfully.")
                    else:
                        print("Server was not ready to receive the file.")
                except FileNotFoundError:
                    print(f"File '{filename}' not found on client side.")
                
            elif command == "QUIT":
                break

    except BrokenPipeError:
        print("Connection to server was unexpectedly closed.")
    finally:
        client_socket.close()
        print("Connection closed")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python ftp_client.py <server_address> <server_port>")
        sys.exit(1)
    
    server_address = sys.argv[1]
    server_port = int(sys.argv[2])
    
    ftp_client(server_address, server_port)
