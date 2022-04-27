# Astronomy Picture Of the Day

import asyncio
import contextvars
import logging
import os
import time
from os import makedirs
from shutil import rmtree

import aiofiles
import httpx

API_KEY = os.getenv('NASA_API_KEY')
NASA_APOD_API = f'https://api.nasa.gov/planetary/apod?api_key={API_KEY}'

sema = contextvars.ContextVar('sema')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def duration(func):

    async def _duration_decorator(*args, **kwargs):
        start = time.perf_counter()
        res = await func(*args, **kwargs)
        duration = time.perf_counter() - start
        logger.info(f'{func} took {duration} seconds')
        return res

    return _duration_decorator


@duration
async def get_pictures(count=1):
    sema.set(asyncio.BoundedSemaphore(value=10))
    async with httpx.AsyncClient() as client:
        logger.info(f'get {NASA_APOD_API}')
        response = await client.get(NASA_APOD_API,
                                    params={'count': count},
                                    timeout=10)
        response.raise_for_status()
        tasks = []
        # print(response.content)
        try:
            for item in response.json():
                img_url = item['url']
                if 'https://apod.nasa.gov/apod/image/' not in img_url:
                    continue  # apod also serves youtube urls
                tasks.append(get_and_save(client, img_url))
            await asyncio.wait(tasks)
        except Exception as exc:
            logger.exception(f'exception occurred')


@duration
async def get_and_save(client, img_url):
    async with sema.get():
        img_name, img_response = await get_image(client, img_url)
        await save_images_async(img_name, img_response)


async def get_image(client, img_url: str):
    img_name = img_url.rsplit('/', 1)[1]
    logger.info(f'get {img_url}')
    img_response = await client.get(img_url)
    return img_name, img_response.content


async def save_images_async(img_name, img_bytes):
    async with aiofiles.open(f'nasa_apod/{img_name}', mode='wb') as f:
        logger.info(f'writing to nasa_apod/{img_name}')
        await f.write(img_bytes)


if __name__ == "__main__":
    rmtree('nasa_apod')
    makedirs('nasa_apod', exist_ok=True)
    asyncio.run(get_pictures(count=50))
