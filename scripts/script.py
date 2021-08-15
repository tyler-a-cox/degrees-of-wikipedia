import asyncio
from wikiracer.graph import Graph
from wikiracer.query import is_valid_url, is_valid_wiki

# initialize graph
racer = Graph()

# Coroutines
coroutines = [racer.worker.worker() for _ in range(15)]
start = "Tacos"
end = "Microsoft"

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(racer.shortest_path(start, end), *coroutines)
    )
