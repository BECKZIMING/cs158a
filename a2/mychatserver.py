# mychatserver.py

import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

clients = []
clients_lock = threading.Lock()

def broadcast(message, sender_socket):
    with clients_lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message)
                except:
                    client.close()
                    clients.remove(client)

def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    with clients_lock:
        clients.append(client_socket)

    while True:
        try:
            msg = client_socket.recv(1024)
            if not msg:
                break
            decoded_msg = msg.decode().strip()
            if decoded_msg.lower() == 'exit':
                break
            formatted_msg = f"{client_address[1]}: {decoded_msg}".encode()
            print(formatted_msg.decode())
            broadcast(formatted_msg, client_socket)
        except:
            break

    with clients_lock:
        clients.remove(client_socket)
    client_socket.close()
    print(f"Connection closed: {client_address}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == '__main__':
    main()
