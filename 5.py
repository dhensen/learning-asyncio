import asyncio
import subprocess

condition = asyncio.Condition()


async def wait_for_starts_to_align():
    async with condition:
        print('waiting for the stars to be aligned')
        await condition.wait()
        print('the stars are aligned')


async def align_the_stars():
    print('aligning all starts, this takes a while')
    await condition.acquire()
    await asyncio.sleep(1)
    print('*')
    await asyncio.sleep(1)
    print('*')
    await asyncio.sleep(1)
    print('*')
    condition.notify_all()
    # this also works when used with .notify(n=2) does not work for n=1, I don't yet understand why.
    condition.release()


async def doit(loop):
    return await asyncio.gather(align_the_stars(), wait_for_starts_to_align())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(doit(loop))
