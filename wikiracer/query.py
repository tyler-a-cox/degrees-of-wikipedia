import re
import sys
import logging
import asyncio
import aiohttp
import wikipedia
from .exceptions import RequestException

EXCLUDE = ["Template talk", "Template", "Wikipedia", "Help", "Portal"]

RANDOM_URL = "https://en.wikipedia.org/wiki/Special:Random"
BASE_URL = "https://en.wikipedia.org/w/api.php?"
WIKI_URL = "https://en.wikipedia.org/wiki/"

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


async def request(session, topic, is_source):
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

    cont = None
    titles = []

    while cont != "DONE":
        if is_source:
            response = await _get_links(session, topic, cont)
            cont_type = "plcontinue"
        else:
            response = await _get_linkshere(session, topic, cont)
            cont_type = "lhcontinue"

        _get_titles(response, titles, cont_type)
        try:
            cont = response["continue"][cont_type]
        except KeyError:
            cont = "DONE"

    return titles


async def _get_links(session, topic, cont):
    """
    Helper function for single wiki request.
    """
    payload = {
        "action": "query",
        "titles": topic,
        "prop": "links",
        "format": "json",
        "pllimit": "500",
    }

    if cont:
        payload["plcontinue"] = cont

    # using 'with' closes the session
    async with session.get(BASE_URL, params=payload) as response:
        # check to see if response is OK
        if response.status // 100 == 2:
            return await response.json()
        else:
            print(response.status)
            sys.exit(1)


async def _get_linkshere(session, topic, cont):
    """
    Helper function for single wiki request.
    """
    payload = {
        "action": "query",
        "titles": topic,
        "prop": "linkshere",
        "format": "json",
        "lhlimit": "500",
    }

    if cont:
        payload["lhcontinue"] = cont

    # using 'with' closes the session
    async with session.get(BASE_URL, params=payload) as response:
        # check to see if response is OK
        if response.status // 100 == 2:
            return await response.json()
        else:
            print(response.status)
            sys.exit(1)


"""
async def _get_links(session, topic, cont, prop="links"):

    Helper function for a single wikipedia page request

    Args:
        session:
        topic:
        cont:

    Returns:
        pass

    payload = {
        "action": "query",
        "titles": topic,
        "prop": prop,
        "format": "json",
        "pllimit": "500",
    }

    if cont and prop == "links":
        payload["plcontinue"] = cont

    elif cont and prop == "linkshere":
        payload["lhcontinue"] = cont

    # using 'with' closes the session
    async with session.get(BASE_URL, params=payload) as resp:
        # check to see if response is OK
        if resp.status // 100 == 2:
            return await resp.json()
        else:
            print(resp.status)
            sys.exit(1)
"""


def _get_titles(response, titles, cont_type):
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

    pages = response["query"]["pages"]
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
            if sub["title"].split(":")[0] not in EXCLUDE:
                titles.append(sub["title"])


"""
Synchronous Methods
"""


def request_sync(session, topic, is_source):
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

    cont = None
    titles = []

    while cont != "DONE":
        if is_source:
            response = _get_links_sync(session, topic, cont)
            cont_type = "plcontinue"
        else:
            response = _get_linkshere_sync(session, topic, cont)
            cont_type = "lhcontinue"

        _get_titles_sync(response, titles, cont_type)

        try:
            cont = response["continue"][cont_type]
        except KeyError:
            cont = "DONE"

    return titles


def _get_links_sync(session, topic, cont):
    """
    Helper function for single wiki request.
    """
    payload = {
        "action": "query",
        "titles": topic,
        "prop": "links",
        "format": "json",
        "pllimit": "500",
    }

    if cont:
        payload["plcontinue"] = cont

    # using 'with' closes the session
    with session.get(BASE_URL, params=payload) as response:
        # check to see if response is OK
        return response.json()


def _get_linkshere_sync(session, topic, cont):
    """
    Helper function for single wiki request.
    """
    payload = {
        "action": "query",
        "titles": topic,
        "prop": "linkshere",
        "format": "json",
        "lhlimit": "500",
    }

    if cont:
        payload["lhcontinue"] = cont

    # using 'with' closes the session
    with session.get(BASE_URL, params=payload) as response:
        # check to see if response is OK
        return response.json()


def _get_titles_sync(response, titles, cont_type):
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

    pages = response["query"]["pages"]
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
            if sub["title"].split(":")[0] not in EXCLUDE:
                titles.append(sub["title"])
