import socket
import threading
import os

def client_handler(client_socket):
    """Handle the client's requests."""
    try:
        while True:
            command = client_socket.recv(1024).decode()
            print(f"Received command: {command}")
            
            if command.startswith("STORE"):
                filename = command.split()[1]
                client_socket.sendall(b"READY")  # Notify client that server is ready
                file_data = client_socket.recv(4096)
                with open(filename, 'wb') as f:
                    f.write(file_data)
                print(f"File '{filename}' stored successfully.")
            elif command.startswith("LIST"):
                files = os.listdir('.')
                files_list = '\n'.join(files)
                client_socket.sendall(files_list.encode())
                print("Sent file list to client.")
            elif command.startswith("RETRIEVE"):
                filename = command.split()[1]
                if os.path.exists(filename):
                    client_socket.sendall(b"READY")  # Notify client that server is ready
                    with open(filename, 'rb') as f:
                        file_data = f.read()
                    client_socket.sendall(file_data)
                    print(f"Sent '{filename}' to client.")
                else:
                    client_socket.sendall(b"FILE_NOT_FOUND")
                    print(f"File '{filename}' not found.")
            elif command == "QUIT":
                print("Client requested to end the connection.")
                break
            else:
                print("Invalid command.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
        print("Connection closed with client.")

def start_server(port):
    """Start the FTP server and listen for incoming connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(5)
    print(f"Server is listening on port {port}.")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}.")
            thread = threading.Thread(target=client_handler, args=(client_socket,))
            thread.start()
    except KeyboardInterrupt:
        print("Server is shutting down...")
    finally:
        server_socket.close()
        print("Server closed.")

if __name__ == "__main__":
    PORT = 2121  # Default FTP port or any other unused port
    start_server(PORT)
