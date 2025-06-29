# mychatclient.py

import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 12345


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                print("Server closed the connection.")
                break
            print(message.decode())
        except:
            break

    client_socket.close()
    sys.exit()

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
    except:
        print("Unable to connect to the server.")
        return

    print("Connected to chat server. Type 'exit' to leave.\n")

   
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()

   
    while True:
        message = input()
        if message.strip().lower() == 'exit':
            client_socket.send(message.encode())
            break
        try:
            client_socket.send(message.encode())
        except:
            break

    print("Disconnected from server")
    client_socket.close()

if __name__ == '__main__':
    main()