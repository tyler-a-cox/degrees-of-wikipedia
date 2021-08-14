import sys
import asyncio
from graph import Graph

# initialize graph
racer = Graph()

# Coroutines
coroutines = [racer.fetcher.worker() for _ in range(10)]

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(racer.shortest_path(sys.argv[1], sys.argv[2]), *coroutines)
    )
