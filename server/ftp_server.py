import os
import socket
import threading

def client_handler(client_socket):
    """Handle the client's requests."""
    try:
        while True:
            command = client_socket.recv(1024).decode()
            print(f"Received command: {command}.")

            if command == "QUIT":
                print("Client requested to end the connection.")
                break
            elif command.startswith("LIST"):
                try:
                    files = os.listdir('.')
                    response = '\n'.join(files)
                except Exception as e:
                    response = f"Failed to list directory: {str(e)}"
                client_socket.sendall(response.encode())
            elif command.startswith("RETRIEVE"):
                _, filename = command.split()
                if os.path.exists(filename):
                    with open(filename, 'rb') as file:
                        file_data = file.read()
                        message = f"{len(file_data)}:".encode() + file_data
                    client_socket.sendall(message)
                else:
                    client_socket.sendall(b"0:")
            elif command.startswith("STORE"):
                parts = command.split()
                if len(parts) < 3:
                    client_socket.sendall(b"ERROR")
                    continue
                _, filename, filesize = parts
                filesize = int(filesize)  # Convert the filesize to an integer
                client_socket.sendall(b"READY")
                received_size = 0
                file_data = b""
                # Ensure all data is received based on the filesize
                while received_size < filesize:
                    chunk = client_socket.recv(min(1024, filesize - received_size))
                    if not chunk:
                        break
                    file_data += chunk
                    received_size += len(chunk)
                with open(filename, 'wb') as file:
                    file.write(file_data)
                print(f"File '{filename}' stored successfully.")
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
