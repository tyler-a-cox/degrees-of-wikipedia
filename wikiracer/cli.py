import click
import asyncio
from .graph import Graph

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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(racer.shortest_path(start, end), *coroutines)
    )
