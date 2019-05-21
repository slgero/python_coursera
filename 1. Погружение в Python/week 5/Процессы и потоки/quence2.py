import threading

class Quence:
    """ Очередь, котрая может работать в многопоточной программе"""
    
    def __init__(self, size):
        self.size = size
        self._quence = []
        self._mutex = threading.RLock()
        self._full = threading.Condition(self._mutex)
        self._empty = threading.Condition(self._mutex)
        
    def put(self, val):
        with self._full:
            # Пока у нас слишком большой размер, мы ждём
            while len(self._quence) >= self.size:
                self._full.wait()
            
            self._quence.append(val)
            self._empty.notify()   # Снимаем блокировку для get
            
    def get(self):
        with self._empty:
            while len(self._quence) == 0:
                self._empty.wait()
                
            val = self._quence.pop(0)
            self._full.notify()   # Снимаем блокировку для put
            return val
