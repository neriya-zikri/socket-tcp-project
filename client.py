import socket
import threading

HOST = '127.0.0.1'
PORT = 5555

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode
        except:
            client_socket.close()
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except:
        return

    username = input("Username: ")
    client.send(username.encode)

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.daemon = True
    receive_thread.start()

    while True:
        msg = input(">> ")
        if msg == 'quit':
            break
        client.send(msg.encode)

    client.close()

if __name__ == "__main__":
    start_client()