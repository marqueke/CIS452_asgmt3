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
        
        # error checking if no command has been entered
        command_parts = command.split()
        if not command_parts:
            print("No command has been entered. Please try again.")
            continue
        
        client_socket.send(command.encode())

        if command_parts[0] == "LIST":
            files_list = client_socket.recv(1024).decode()
            print(files_list)
            
        elif command_parts[0] == "RETRIEVE":
            if len(command_parts) < 2:
                print("Usage: RETRIEVE <filename>")
                continue
            filename = command_parts[1]
            file_data = client_socket.recv(1024)
            with open(filename, 'wb') as file:
                file.write(file_data)
            print(f"File '{filename}' retrieved successfully")
            
        elif command_parts[0] == "STORE":
            if len(command_parts) < 2:
                print("Usage: STORE <filename")
                continue
            filename = command_parts[1]
            try:
                with open(filename, 'rb') as file:
                    file_data = file.read()
                # send file size first
                client_socket.send(file_data)
                print(f"File '{filename}' stored successfully")
            except FileNotFoundError:
                print(f"File '{filename}' not found.")
                
        elif command_parts[0] == "QUIT":
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

