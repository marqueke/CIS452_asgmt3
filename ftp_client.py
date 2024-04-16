import socket
import sys

def connect_to_server(server_address, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, server_port))
    return client_socket

def ftp_client(server_address, server_port):
    client_socket = connect_to_server(server_address, server_port)
    print("Connected to server")

    while True:
        command = input("Enter command: ")
        client_socket.send(command.encode())

        if command.startswith("LIST"):
            files_list = client_socket.recv(1024).decode()
            print(files_list)
        elif command.startswith("RETRIEVE"):
            # Check if the command has at least two parts separated by space
            parts = command.split()
            if len(parts) < 2:
                print("Invalid command. Usage: RETRIEVE filename")
                continue

            filename = parts[1]
            with open(filename, 'wb') as file:
                while True:
                    file_data = client_socket.recv(1024)
                    if not file_data:
                        break
                    file.write(file_data)
            print("File '{}' retrieved successfully".format(filename))  # Moved print statement
        elif command.startswith("STORE"):
            filename = command.split()[1]
            with open(filename, 'rb') as file:
                file_data = file.read()
            client_socket.send(file_data)
            print("File '{}' stored successfully".format(filename))
        elif command.startswith("QUIT"):
            client_socket.close()
            break
        else:
            print("Invalid command")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python ftp_client.py <server_address> <server_port>")
        sys.exit(1)
    
    server_address = sys.argv[1]
    server_port = int(sys.argv[2])
    
    ftp_client(server_address, server_port)

