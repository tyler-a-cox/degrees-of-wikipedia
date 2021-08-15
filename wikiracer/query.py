import re
import sys
import logging
import asyncio
import aiohttp
import wikipedia

RANDOM_URL = "https://en.wikipedia.org/wiki/Special:Random"
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


def is_valid_wiki(url: str) -> bool:
    """
    Verifies that the url passed is a valid wikipedia link

    Args:
        url: str
            URL of the wikipedia page to be queried

    Returns:
        bool
    """
    return


def is_valid_url(url: str) -> bool:
    """
    Verifies that the url passed is a valid url

    Args
    """
    match = re.match(regex, url)
    return match is not None


async def request(session: aiohttp.ClientSession, topic: str, is_source):
    """
    Sends wiki request to obtain links for a topic.
    Due to a 500 link limit, additional requests must be sent based on the
    'continue' response.

    Args:
        session
        topic
        is_source

    Returns:
        titles: list
    """

    cont = True
    titles = []

    while cont:
        if is_source:
            body = await _get_links(session, topic, cont)
            cont_type = "plcontinue"
        else:
            body = await _get_links(session, topic, cont, prop="linkshere")
            cont_type = "lhcontinue"

        _get_titles(body, titles, cont_type)
        try:
            cont = body["continue"][cont_type]
        except KeyError:
            cont = False

    return titles


async def _get_links(session, topic, cont, prop="links"):
    """
    Helper function for a single wikipedia page request

    Args:
        session:
        topic:
        cont:

    Returns:
        pass
    """
    payload = {
        "action": "query",
        "titles": topic,
        "prop": prop,
        "format": "json",
        "pllimit": "500",
    }

    if cont:
        payload["plcontinue"] = cont

    # using 'with' closes the session
    async with session.get(BASE_URL, params=payload) as resp:
        # check to see if response is OK
        if resp.status // 100 == 2:
            return await resp.json()
        else:
            print(resp.status)
            sys.exit(1)


def _get_titles(body, titles, cont_type):
    """
    Adds titles from response to list.
    Responses typically have one page of links, but accounted for several in
    case.

    Args:
        body
        titles:
        cont_type:

    Returns:
        Pass
    """

    pages = body["query"]["pages"]
    links = []
    if cont_type == "plcontinue":
        link_type = "links"
    else:
        link_type = "linkshere"

    for page in pages:
        if link_type in pages[page]:
            links.append(pages[page][link_type])

    for link in links:
        for sub in link:
            titles.append(sub["title"])
