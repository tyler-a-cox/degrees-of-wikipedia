import re
import sys
import asyncio
import aiohttp
import wikipedia

BASE_URL = "https://en.wikipedia.org/w/api.php?"
WIKI_URL = "https://en.wikipedia/wiki/"

regex = re.compile(
    r"^(?:http|ftp)s?://"  # http:// or https://
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
    r"localhost|"  # localhost...
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)


def is_valid_url(url: str) -> bool:
    """
    """
    match = re.match(regex, url)
    return match is not None


"""
Asychronous Methodss
"""


async def request(session: aiohttp.ClientSession, topic: str) -> list[str]:
    """
    """
    pass


"""
Synchronous Methods
"""


def fetch_links(topic: str) -> list[str]:
    """
    """
    if not isinstance(topic, str):
        raise TypeError("Input must be a url or topic name")

    if is_valid_url(topic):
        url = topic

    else:
        topic = topic.replace(" ", "_")
        url = os.path.join(WIKI_URL, topic)

    try:
        page = wikipedia.page(topic)
        links = page.links

    except KeyError:
        links = []

    return links
