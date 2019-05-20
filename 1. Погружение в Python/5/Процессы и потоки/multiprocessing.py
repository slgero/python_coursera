# Создание процессора, модуль multiprocessing
from multiprocessing import Process

class PrintProcess(Process):
    def __init__(self, name):
        super().__init__()
        self.name = name
        
    def run(self):
        # переопределяем метод
        print(f'Hello, {name}!')
        
p = PrintProcess('Bob')
p.start()
p.join()
