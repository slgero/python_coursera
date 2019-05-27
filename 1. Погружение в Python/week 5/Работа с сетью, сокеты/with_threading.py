# обработка нескольких соединений, потоки

import socket
import threading

def process_requests(conn, addr):
    print(f'connected cliaen {addr}')
    with conn:
        while True:
            data = conn.recv(1024)
            if data:
                print('Data =', data.decode("utf8"))
            else:
                break

# создаём сокет
with socket.socket() as sock:
    sock.bind(("", 10001)) # Ассоциируем сокет с нужным портом
    sock.listen()
    while True:
        # в бесконечном цикле принимаем входящее соединение
        conn, addr = sock.accept()
        # создаём поток
        th = threading.Thread(target=process_requests, args=(conn, addr))
        th.start()
