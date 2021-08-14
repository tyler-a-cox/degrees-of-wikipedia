from .query import *
from .graph import *
from .fetch import *
from .analysis import *
from .database import *

# initialize graph
racer = Graph()

# Coroutines
coroutines = [racer.fetcher.worker() for _ in range(15)]


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(racer.shortest_path(sys.argv[1], sys.argv[2]), *coroutines)
    )
