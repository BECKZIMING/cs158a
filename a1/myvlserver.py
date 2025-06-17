# myvlserver.py
import socket

def receive_full_message(conn):
    length_header = conn.recv(2).decode()
    if not length_header:
        return None
    msg_len = int(length_header)
    print(f"msg_len: {msg_len}")

    data = b''
    while len(data) < msg_len:
        to_read = min(64, msg_len - len(data))
        part = conn.recv(to_read)
        if not part:
            break
        data += part

    original = data.decode()
    print(f"processed: {original}")
    return length_header + original

def run_server(host='0.0.0.0', port=12000):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((host, port))
    serverSocket.listen(5)
    print(f"Server is listening on port {port}...")

    while True:
        conn, addr = serverSocket.accept()
        print(f"Connected from {addr[0]}")

        full_message = receive_full_message(conn)
        if full_message:
            msg_len = full_message[:2]
            body = full_message[2:]
            response = msg_len + body.upper()
            conn.sendall(response.encode())
            print(f"msg_len_sent: {msg_len}")
        conn.close()
        print("Connection closed\n")

if __name__ == '__main__':
    run_server()
