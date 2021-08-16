import aiohttp
import asyncio
from .query import request


class Session:
    """
    """

    def __init__(self):
        self.to_fetch = asyncio.Queue()

    async def worker(self):
        async with aiohttp.ClientSession() as session:
            while True:
                (
                    title_to_fetch,
                    queue_links,
                    depth,
                    is_source,
                ) = await self.to_fetch.get()
                resp = await request(session, title_to_fetch, is_source)
                await queue_links(title_to_fetch, resp, depth, is_source)

    async def producer(self, topic, queue_links, depth, is_source):
        await self.to_fetch.put((topic, queue_links, depth, is_source))
