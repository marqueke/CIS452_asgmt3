import os
import socket
import threading

def client_connection(client_socket):
    try:
        while True:
            command = client_socket.recv(1024).decode()
            if not command:
                break  # close client connection
            print(f"Received command: {command}")
            if command.startswith("LIST"):
                files = os.listdir('.')
                files_list = '\n'.join(files)
                client_socket.sendall(files_list.encode())
            elif command.startswith("RETRIEVE"):
                filename = command.split()[1]
                try:
                    with open(filename, 'rb') as f:
                        data = f.read()
                        client_socket.sendall(data)
                except FileNotFoundError:
                    client_socket.sendall(b"Error. File not found.")
            elif command.startswith("STORE"):
                filename = command.split()[1]
                # client sends file size first for file transfer
                file_data = client_socket.recv(1024)
                with open(filename, 'wb') as f:
                    while file_data:
                        f.write(file_data)
                        client_socket.settimeout(1) # timeout to detect end of file
                        try:
                            file_data = client_socket.recv(1024)
                        except socket.timeout:
                            break
                print(f"File '{filename}' stored successfully")
            elif command == "QUIT":
                client_socket.sendall(b"Connection closed.")
                break
    finally:
        client_socket.close()
        print("Connection with client socket has been closed.")

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(5)
    print(f"FTP server is listening on port {port}...")
    
    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connected to {addr}")
            client_thread = threading.Thread(target=client_connection, 
                                             args=(client_socket,))
            client_thread.start()
    except KeyboardInterrupt:
        server_socket.close()
        print("The server has stopped.")

if __name__ == "__main__":
    PORT = 2121 # example port
    start_server(PORT)