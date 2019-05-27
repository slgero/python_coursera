# обработка нескольких соединений одновременно, процессы и потоки


# При запуске на ПК выпадает ошибка: Обычно разрешается только одно использование адреса сокета (протокол/сетевой адрес/порт)

import socket
import multiprocessing
import threading
import os

def process_requests(conn, addr):
    print(f'connected client {addr}')
    with conn:
        while True:
            data = conn.recv(1024)
            if data:
                print('Data =', data.decode("utf8"))
            else:
                break

# каждый worker запущен в отдельном процессе
def worker(sock):
    while True:
        print(f'Pid = {os.getpid()}')
        conn, addr = sock.accept()
        th = threading.Thread(target=process_requests, args=(conn, addr))
        th.start()

with socket.socket() as sock:
    sock.bind(("", 10001))
    sock.listen()

    # при создании нового процесса, мы полностью копируем socket
    workers_count = 3
    workers_list = [multiprocessing.Process(target=worker, args=(sock,))
                   for _ in range(workers_count)]

    for w in workers_list:
        w.start()

    for w in workers_list:
        w.join()
