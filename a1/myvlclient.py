from socket import *

# Server info
serverName = 'localhost'
serverPort = 12000

# Create TCP socket
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Get user input (includes 2-digit length prefix)
sentence = input("Input lowercase sentence (e.g., 10helloworld): ")

# Send the full message
clientSocket.send(sentence.encode())

# Receive data in chunks
data = b''
msg_len = int(sentence[:2])  # Extract intended message length
while len(data) < msg_len:
    chunk = clientSocket.recv(64)
    if not chunk:
        break
    data += chunk

print("From Server:", data.decode())
clientSocket.close()