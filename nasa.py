# Astronomy Picture Of the Day
NASA_APOD_API = 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY'

import asyncio
from os import makedirs
from shutil import rmtree
import time
import httpx
import logging

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
    async with httpx.AsyncClient() as client:
        response = await client.get(NASA_APOD_API, params={'count': count})
        for item in response.json():
            img_url = item['url']
            img_name = img_url.rsplit('/', 1)[1]
            img_response = await client.get(img_url)
            with open(f'nasa_apod/{img_name}', mode='wb') as fp:
                fp.write(img_response.content)


if __name__ == "__main__":
    rmtree('nasa_apod')
    makedirs('nasa_apod', exist_ok=True)
    asyncio.run(get_pictures(count=10))
