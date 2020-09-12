import time
import aiohttp
import asyncio


async def search(session, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/85.0.4183.102 Safari/537.36',
    }

    async with session.post(url, headers=headers) as response:
        res, status_code = await response.text(), response.status
    print(status_code)


async def search_all(urls):
    st = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [search(session, url) for url in urls]
        await asyncio.gather(*tasks)
    print('time taken:', time.time() - st)


links = [
    'https://www.kijiji.ca/b-canada/honda-z50/k0l0',
    'https://www.kijiji.ca/b-canada/honda-z50r/k0l0',
    'https://www.kijiji.ca/b-canada/honda-z-50/k0l0',
    'https://www.kijiji.ca/b-canada/honda-z-50r/k0l0',
    'https://www.kijiji.ca/b-canada/honda-z50-r/k0l0',
    'https://www.kijiji.ca/b-canada/honda-mini-trail/k0l0',
    'https://www.kijiji.ca/b-canada/honda-mini-moto/k0l0',
    'https://www.kijiji.ca/b-canada/honda-50cc/k0l0',
    'https://www.kijiji.ca/b-canada/honda-ct/k0l0',
    'https://www.kijiji.ca/b-canada/honda-ct-70/k0l0',
    'https://www.kijiji.ca/b-canada/honda-qr-50/k0l0',
    'https://www.kijiji.ca/b-canada/honda-atc/k0l0',
    'https://www.kijiji.ca/b-canada/honda-mini-bike/k0l0',
    'https://www.kijiji.ca/b-ontario/honda-crf/k0l9004',
    'https://www.kijiji.ca/b-quebec/honda-crf/k0l9001',
    'https://www.kijiji.ca/b-quebec/honda-trx/k0l9001',
    'https://www.kijiji.ca/b-ontario/honda-trx/k0l9004',
    'https://www.kijiji.ca/b-canada/honda-trx-70/k0l0',
    'https://www.kijiji.ca/b-ontario/kawasaki-kfx/k0l9004',
    'https://www.kijiji.ca/b-quebec/kawasaki-kfx/k0l9001',
    'https://www.kijiji.ca/b-quebec/kawasaki-50cc/k0l9001',
    'https://www.kijiji.ca/b-ontario/kawasaki-50cc/k0l9004',
    'https://www.kijiji.ca/b-ontario/kawasaki-90cc/k0l9004',
    'https://www.kijiji.ca/b-quebec/kawasaki-90cc/k0l9001',
    'https://www.kijiji.ca/b-quebec/suzuki-lt/k0l9001',
    'https://www.kijiji.ca/b-ontario/suzuki-lt/k0l9004',
    'https://www.kijiji.ca/b-ontario/suzuki-50cc/k0l9004',
    'https://www.kijiji.ca/b-quebec/suzuki-50cc/k0l9001',
    'https://www.kijiji.ca/b-quebec/suzuki-ltz/k0l9001',
    'https://www.kijiji.ca/b-ontario/suzuki-ltz/k0l9004',
    'https://www.kijiji.ca/b-ontario/yamaha-ttr/k0l9004',
    'https://www.kijiji.ca/b-quebec/yamaha-ttr/k0l9001',
    'https://www.kijiji.ca/b-quebec/yamaha-raptor/k0l9001',
    'https://www.kijiji.ca/b-ontario/yamaha-raptor/k0l9004',
    'https://www.kijiji.ca/b-ontario/yamaha-pw/k0l9004',
    'https://www.kijiji.ca/b-quebec/yamaha-pw/k0l9001',
    'https://www.kijiji.ca/b-quebec/polaris-outlaw/k0l9001',
    'https://www.kijiji.ca/b-ontario/polaris-outlaw/k0l9004',
    'https://www.kijiji.ca/b-ontario/bombardier-tundra/k0l9004',
    'https://www.kijiji.ca/b-quebec/bombardier-tundra/k0l9001',
    'https://www.kijiji.ca/b-quebec/ski-doo-tundra/k0l9001',
    'https://www.kijiji.ca/b-ontario/ski-doo-tundra/k0l9004',
    'https://www.kijiji.ca/b-ontario/skidoo-tundra/k0l9004',
    'https://www.kijiji.ca/b-quebec/skidoo-tundra/k0l9001',
    'https://www.kijiji.ca/b-quebec/yamaha-bravo/k0l9001',
    'https://www.kijiji.ca/b-ontario/yamaha-bravo/k0l9004',
    'https://www.kijiji.ca/b-quebec/ds90/k0l9001',
    'https://www.kijiji.ca/b-ontario/ds90/k0l9004',
    'https://www.kijiji.ca/b-canada/porsche/k0l0',
    'https://www.kijiji.ca/b-canada/560sl/k0l0',
    'https://www.kijiji.ca/b-classic-cars/canada/mercedes/k0c122l0',
    'https://www.kijiji.ca/b-classic-cars/canada/jaguar/k0c122l0?rb=true',
    'https://www.kijiji.ca/b-classic-cars/canada/bmw/k0c122l0',
    'https://www.kijiji.ca/b-classic-cars/canada/ferrari/k0c122l0?rb=true',
    'https://www.kijiji.ca/b-classic-cars/canada/corvette/k0c122l0?rb=true',
]

asyncio.run(search_all(links))
