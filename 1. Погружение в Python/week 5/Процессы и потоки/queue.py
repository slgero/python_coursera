# Очереди, модуль queue
from queue import Queue
from threading import Thread

def worker(q, n):
    while True:
        item = q.get()
        if item is None:
            break
        print("process data:", n, item)

q = Queue(5)
th1 = Thread(target=worker, args=(q, 1))
th2 = Thread(target=worker, args=(q, 2))
# Запускаем два бесконечных потока
th1.start(); th2.start()

# Заполняем очередь
for i in range(50):
    q.put(i)

# При None - выход из бесконечного цикла
q.put(None); q.put(None)

# Закрываем потоки
th1.join(); th2.join()
