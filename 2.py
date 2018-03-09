import asyncio

loop = asyncio.get_event_loop()


async def hello():
    print('hello')
    await asyncio.sleep(3)
    print('world')


async def doit(loop):
    """
    Pass in the loop and call create_task instead of asyncio.ensure_future
    """
    tasks = [loop.create_task(hello()) for i in range(1, 10)]
    await asyncio.wait(tasks)


if __name__ == '__main__':
    loop.run_until_complete(doit(loop))
