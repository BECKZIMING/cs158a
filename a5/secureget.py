import socket
import ssl

# Set the target hostname and port (HTTPS uses port 443)
hostname = 'www.google.com'
port = 443

# Create a TCP socket and establish SSL context
context = ssl.create_default_context()
with socket.create_connection((hostname, port)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print(f"SSL established. Protocol: {ssock.version()}")

        # Construct an HTTP GET request (note the \r\n line endings)
        request = f"GET / HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n"
        ssock.send(request.encode())

        # Receive the response in chunks
        response = b""
        while True:
            data = ssock.recv(4096)
            if not data:
                break
            response += data

# Decode the full response and separate headers from the HTML body
response_str = response.decode(errors='ignore')
header, _, body = response_str.partition('\r\n\r\n')

# Save the HTML content to a file
with open("response.html", "w", encoding="utf-8") as f:
    f.write(body)
