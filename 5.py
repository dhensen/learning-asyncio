import asyncio
import subprocess


async def wait_for_stars_to_align(condition):
    print('waiting for the stars to be aligned')
    async with condition:
        print('the stars are aligned')


async def align_the_stars(condition):
    print('aligning all starts, this takes a while')
    async with condition:
        await asyncio.sleep(1)
        print('*')
        await asyncio.sleep(1)
        print('*')
        await asyncio.sleep(1)
        print('*')
        condition.notify(n=1)


async def doit(loop):
    condition = asyncio.Condition()
    return await asyncio.wait([
        align_the_stars(condition),
        wait_for_stars_to_align(condition),
    ])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(doit(loop))
