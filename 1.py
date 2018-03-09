import asyncio

loop = asyncio.get_event_loop()


async def hello():
    print('hello')
    await asyncio.sleep(3)
    print('world')


async def doit():
    tasks = [asyncio.ensure_future(hello()) for i in range(1, 10)]
    await asyncio.wait(tasks)


if __name__ == '__main__':
    loop.run_until_complete(doit())
