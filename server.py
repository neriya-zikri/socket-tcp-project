import socket
import threading

HOST = '127.0.0.1'
PORT = 5555

clients = {}

def handle_client(client_socket):
    username = None
    try:
        username = client_socket.recv(1024).decode()
        
        if username in clients:
            client_socket.send("Username taken".encode())
            client_socket.close()
            return
        
        clients[username] = client_socket
        client_socket.send(f"Welcome {username}".encode())

        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            
            if ':' in message:
                target_name, msg_content = message.split(':', 1)
                if target_name in clients:
                    target_socket = clients[target_name]
                    full_msg = f"[{username}]: {msg_content}"
                    target_socket.send(full_msg.encode())
                else:
                    client_socket.send("User not found".encode())
            else:
                client_socket.send("Invalid format".encode())

    except:
        pass
    finally:
        if username and username in clients:
            del clients[username]
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    
    while True:
        client_sock, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_sock,))
        thread.start()

if __name__ == "__main__":
    start_server()