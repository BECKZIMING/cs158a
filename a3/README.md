# CS158A A3 - Leader Election

## How to Run

1. Open 3 terminal windows.
2. In each terminal, navigate into node3, node2, node1 respectively.
3. In node3 terminal, run:
   python3 myleprocess.py
4. Then run node2:
   python3 myleprocess.py
5. Finally, run node1:
   python3 myleprocess.py

Wait ~20 seconds for election to complete.
Each node will log output to log.txt.

terminal：

node1:
(base) beckwang@MacBook-Pro node1 % python3 myleprocess.py
[3313bae8] Trying to connect to 127.0.0.1:5002 ...
[3313bae8] ✅ Connected to 127.0.0.1:5002

node2:
[20f099bd] Trying to connect to 127.0.0.1:5003 ...
[20f099bd] ✅ Connected to 127.0.0.1:5003

node3:

(base) beckwang@MacBook-Pro node3 % python3 myleprocess.py
[ca5b9ff5] Trying to connect to 127.0.0.1:5001 ...
[ca5b9ff5] ✅ Connected to 127.0.0.1:5001
Election finished. Leader is ca5b9ff5-af20-4253-b9df-4a1ed4d1dba4


Sent: uuid=ca5b9ff5-af20-4253-b9df-4a1ed4d1dba4, flag=1
Waiting to propagate flag=1...
Received: uuid=ca5b9ff5-af20-4253-b9df-4a1ed4d1dba4, flag=0, same, 1, leader_id=ca5b9ff5-af20-4253-b9df-4a1ed4d1dba4
