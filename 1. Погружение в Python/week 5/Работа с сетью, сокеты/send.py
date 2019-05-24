import socket

with socket.create_connection(("127.0.0.1", 10001)) as sock:
    for i in range(10):
        sock.sendall(str(i).encode("utf8"))
