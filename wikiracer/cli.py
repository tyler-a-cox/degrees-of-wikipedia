import click
import asyncio
from .graph import Graph

# initialize graph
racer = Graph()

# Coroutines
coroutines = [racer.fetcher.worker() for _ in range(15)]


@click.command()
@click.option("--start", is_flag=True, help="Start topic")
@click.option("--end", is_flag=True, help="End topic?")
def main(start, end):
    """
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(racer.shortest_path(sys.argv[1], sys.argv[2]), *coroutines)
    )
