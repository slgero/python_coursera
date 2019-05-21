# Создание процесса на Python

import time
import os

pid = os.fork()  # Availability: Unix
if pid == 0:
    # дочерний процесс
    while True:
        print('child:', os.getpid())
        time.sleep(5)
else:
    # родительский процесс
    while True:
        print('parrent:', os.getpid)
        time.sleep(3)
    
