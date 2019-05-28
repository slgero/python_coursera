import asyncio

# простейшая корутина
async def foo():
    print('FOO: Hey, I am foo!')
    # Используя await в какой-либо корутине, мы таким образом объявляем,
    # что корутина может отдавать управление обратно в event loop, который,
    # в свою очередь, запустит какую-либо следующую задачу: kek.
    await asyncio.sleep(0)
    print('FOO: foo is returned, bitches!')

# простейшая корутина
async def kek():
    print('KEK: kek kek kek!')
    await asyncio.sleep(0)
    print('KEK: KEK IS AWESOME')

# простейшая корутина
async def lol():
    print('LOL: It\'s beautiful LOL')
    await asyncio.sleep(1)
    print('LOL: I waited a full second! ')

# Создаём новый цикл событий
loop = asyncio.get_event_loop()

# Корутины могут быть запущены только из другой корутины, или обёрнуты в задачу с помощью create_task
tasks = [loop.create_task(foo()), loop.create_task(kek()), loop.create_task(lol())]

# После того, как у нас оказались 3 задачи, объединим их, используя wait
wait_tasks = asyncio.wait(tasks)

# И, наконец, отправим на выполнение в цикл событий через run_until_complete
loop.run_until_complete(wait_tasks)
loop.close()


# вывод:
# FOO: Hey, I am foo!
# KEK: kek kek kek!
# LOL: It's beautiful LOL
# FOO: foo is returned, bitches!
# KEK: KEK IS AWESOME
# LOL: I waited a full second!
