 CS158A Project A2 - Multi-Client Chat System

This project implements a basic multi-client chat server using Python TCP sockets and threading.  
Each client can send and receive messages to/from all other connected clients, excluding themselves.

---

 📦 Files

- `mychatserver.py`: The chat server. Accepts connections and relays messages.
- `mychatclient.py`: The chat client. Connects to server and allows chat.
- `README.md`: This file, with instructions and example.

---

 🚀 How to Run

 1. Start the Server

Open a terminal and run:

```bash
cd a2
python3 mychatserver.py


💬 Example Execution

Terminal 1 (Server)
Server listening on 127.0.0.1:12345
New connection from ('127.0.0.1', 52890)
New connection from ('127.0.0.1', 52891)

Terminal 2 (Client 1)
Connected to chat server. Type 'exit' to leave.

hello from client 1
52891: hi!
exit
Disconnected from server

Terminal 3 (Client 2)
Connected to chat server. Type 'exit' to leave.

52890: hello from client 1
hi!
52890: exit
Disconnected from server