# Создание сокета, сервер

import socket

# https://docs.python.org/3/library/socket.html
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Создаём сокет
sock.bind(('127.0.0.1', 10001)) # Ассоциируем сокет с нужным портом
sock.listen(socket.SOMAXCONN)

conn, addr = sock.accept() # Разрешаем принять чей-то connect()
# conn - полнодуплексный канал
while True:
    data = conn.recv(1024) # 1024 is bufsize
    if not data:
        break
    print(data.decode("utf8"))
conn.close()
sock.close()
