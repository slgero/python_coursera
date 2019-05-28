import random
import asyncio
from time import sleep

def task(pid):
    """Synchronous non-deterministic task
    """
    sleep(random.randint(0,2)*0.0001)
    print(f'Task {pid} is done!')

async def task_coro(pid):
    """Coroutine non-deterministic task
    """
    await asyncio.sleep(random.randint(0,2)*0.0001)
    print(f'Task {pid} is done!')

def synchronous():
    for i in range(1, 10):
        task(i)

async def asynchronous():
    tasks = [asyncio.create_task(task_coro(i)) for i in range(1,10)]
    await asyncio.wait(tasks)

print('Synchronous')
synchronous()

ioloop = asyncio.get_event_loop()
print('Asynchronous')
ioloop.run_until_complete(asynchronous())
ioloop.close()

# Вывод:

# Synchronous
# Task 1 is done!
# Task 2 is done!
# Task 3 is done!
# Task 4 is done!
# Task 5 is done!
# Task 6 is done!
# Task 7 is done!
# Task 8 is done!
# Task 9 is done!
# Asynchronous
# Task 2 is done!
# Task 9 is done!
# Task 1 is done!
# Task 7 is done!
# Task 8 is done!
# Task 3 is done!
# Task 5 is done!
# Task 6 is done!
# Task 4 is done!
