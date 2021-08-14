import aiohttp
import asyncio
from query import request


class Session:
    """
    """

    def __init__(self):
        self.to_fetch = asyncio.Queue()

    async def worker(self):
        async with aiohttp.ClientSession() as session:
            while True:
                title_to_fetch, cb, depth, is_source = await self.to_fetch.get()
                resp = await request(session, title_to_fetch, is_source)
                await cb(title_to_fetch, resp, depth, is_source)

    async def producer(self, topic, cb, depth, is_source):
        await self.to_fetch.put((topic, cb, depth, is_source))
