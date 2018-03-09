import asyncio
import subprocess


async def run(command):
    process = await asyncio.create_subprocess_exec(
        *command,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    return await process.wait()


async def hello():
    print('hello')
    # await asyncio.sleep(3)
    res = await run(['/usr/bin/sleep', '3'])
    print('world')


async def doit(loop):
    """
    Pass in the loop and call create_task instead of asyncio.ensure_future
    """
    tasks = [hello() for i in range(1, 10)]
    await asyncio.wait(tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(doit(loop))
