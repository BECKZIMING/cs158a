import socket
import ssl

hostname = 'www.google.com'
port = 443

# 创建默认 SSL 上下文
context = ssl.create_default_context()

# 建立 socket 连接
with socket.create_connection((hostname, port)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        # 发送 HTTP GET 请求
        request = "GET / HTTP/1.1\r\nHost: www.google.com\r\nConnection: close\r\n\r\n"
        ssock.sendall(request.encode())

        # 接收完整响应
        response = b""
        while True:
            data = ssock.recv(4096)
            if not data:
                break
            response += data

        # 保存到文件（只保存 HTML 部分）
        with open("response.html", "wb") as f:
            f.write(response)
