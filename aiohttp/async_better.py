import aiohttp
import asyncio
import time

start_time = time.time()


async def get_pokemon(session, url):
    async with session.get(url) as resp:
        pokemon = await resp.json()
        return pokemon["name"]


async def main():

    async with aiohttp.ClientSession() as session:

        tasks = []
        for number in range(1, 500):
            url = f"https://pokeapi.co/api/v2/pokemon/{number}"
            tasks.append(asyncio.ensure_future(get_pokemon(session, url)))

        original_pokemon = await asyncio.gather(*tasks)
        return original_pokemon


pokemon = asyncio.run(main())
print(pokemon)
print("--- %s seconds ---" % (time.time() - start_time))
