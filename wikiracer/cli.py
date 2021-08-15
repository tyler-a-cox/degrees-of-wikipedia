import click
import asyncio
from .graph import Graph
from .query import is_valid_url, is_valid_wiki

# initialize graph
racer = Graph()

# Coroutines
coroutines = [racer.worker.worker() for _ in range(15)]


@click.command()
@click.argument("start", type=str)
@click.argument("end", type=str)
def main(start, end):
    """
    """
    if is_valid_url(start) and is_valid_url(end):
        pass
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(racer.shortest_path(start, end), *coroutines)
    )
