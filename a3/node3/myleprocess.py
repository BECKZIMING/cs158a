import socket
import threading
import uuid
import json
import time
client = None 
time.sleep(3)

my_id = str(uuid.uuid4())
leader_id = None
found_leader = False
log_lock = threading.Lock()

def log(msg):
    with log_lock:
        with open("log.txt", "a") as f:
            f.write(msg + "\n")

log(f"My UUID: {my_id}")

# Load config
with open("config.txt") as f:
    lines = f.read().splitlines()
    my_host, my_port = lines[0].split(",")
    next_host, next_port = lines[1].split(",")
    my_port = int(my_port.strip())
    next_port = int(next_port.strip())

def make_msg(uid, flag):
    return json.dumps({"uuid": uid, "flag": flag}) + "\n"

def parse_msg(data):
    return json.loads(data)

def server_thread(conn):
    global found_leader, leader_id
    buffer = ""
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            buffer += data
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                msg = parse_msg(line)
                status = "greater" if msg["uuid"] > my_id else ("less" if msg["uuid"] < my_id else "same")
                log(f"Received: uuid={msg['uuid']}, flag={msg['flag']}, {status}, {int(found_leader)}, leader_id={leader_id if leader_id else 'None'}")
                
                if found_leader:
                    if msg["flag"] == 1 and msg["uuid"] != my_id:
                        send_msg(msg["uuid"], 1)
                    elif msg["flag"] == 1 and msg["uuid"] == my_id:
                        log("Received flag=1 for self (done)")
                else:
                    if msg["uuid"] == my_id:
                        found_leader = True
                        leader_id = my_id
                        log(f"Leader is decided to {leader_id}")
                        send_msg(leader_id, 1)
                    elif msg["uuid"] > my_id:
                        send_msg(msg["uuid"], 0)
                    else:
                        log(f"Ignored: uuid={msg['uuid']}, flag={msg['flag']}")
        except Exception as e:
            log(f"[Server Error] {e}")
            break

def send_msg(uid, flag):
    global client
    try:
        msg = make_msg(uid, flag)
        client.send(msg.encode())
        log(f"Sent: uuid={uid}, flag={flag}")
        time.sleep(0.1)
    except Exception as e:
        log(f"[Send Error] {e}")

def start_server():
    try:
        conn, _ = server.accept()
        server_thread(conn)
    except Exception as e:
        log(f"[Accept Error] {e}")

# Start server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((my_host, my_port))
server.listen(1)
threading.Thread(target=start_server).start()

# Wait a bit before client tries to connect
time.sleep(3)

# Connect to next node
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        print(f"[{my_id[:8]}] Trying to connect to {next_host}:{next_port} ...")
        client.connect((next_host, next_port))
        print(f"[{my_id[:8]}] ✅ Connected to {next_host}:{next_port}")
        break
    except Exception as e:
        print(f"[{my_id[:8]}] ❌ Retry: {e}")
        time.sleep(1)

# Delay before sending initial UUID
time.sleep(1.5)
send_msg(my_id, 0)

# Wait up to 60s for election
for _ in range(60):
    if found_leader:
        break
    time.sleep(1)

# Extra wait for flag=1 propagation
if found_leader:
    log("Waiting to propagate flag=1...")
    time.sleep(10)
else:
    log("Timeout: Leader not found")

client.close()
server.close()
print(f"Election finished. Leader is {leader_id}")
