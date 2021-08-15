import sys
import asyncio
import logging
from queue import Queue
from .query import request
from .fetch import Session
from .utils import save_graph


class Graph:
    """
    A Wikipedia page and its outlinks stored as a graph.
    """

    def __init__(self, is_source: bool = True):
        """
        Args:
            is_source: bool
        """
        self.graph = {}
        self.worker = Session()
        self.to_visit_start = asyncio.Queue()
        self.to_visit_end = asyncio.Queue()
        self.came_from_start = {}
        self.came_from_end = {}
        self.logger = logging.getLogger()

    async def shortest_path(self, start, end):
        """
        A breadth-first search for a path between a start and end topic.

        Args:
            start
            end

        Returns:
            None
        """
        if start == end:
            logger.info([start])
            sys.exit(0)

        # initialize came_from with start node to trace back
        self.came_from_start[start] = None
        self.came_from_end[end] = None

        # push start, depth=0 onto queue
        await self.to_visit_start.put((start, 0))
        await self.to_visit_end.put((end, 0))

        while True:
            await self.bfs(
                self.to_visit_start,
                self.came_from_start,
                self.came_from_end,
                is_source=True,
            )
            await self.bfs(
                self.to_visit_end,
                self.came_from_end,
                self.came_from_start,
                is_source=False,
            )

        logger.info("No path found")
        sys.exit(0)

    async def bfs(self, to_visit, came_from, dest_cf, is_source):
        """

        Args:
            to_visit
            came_from
            dest_cf
            is_source
        """
        cur, depth = await to_visit.get()

        # if current topic is found in the opposing topic's visited,
        # then path exists and must be traced back on both sides to return
        if cur in dest_cf:
            print(is_source)
            path1 = self.find_path(came_from, cur)
            path2 = self.find_path(dest_cf, cur)

            if is_source:
                path1.reverse()
                path1.pop()
                path1.extend(path2)
                print(path1)
                save_graph(self.graph)
                self.logger.info(path1)
            else:
                path2.reverse()
                path2.pop()
                path2.extend(path1)
                print(path2)
                save_graph(self.graph)
                self.logger.info(path2)

            sys.exit(0)

        # condition set to not exceed 20 depths of search
        if depth == 20:
            logger.info("Path not found")
            sys.exit(0)

        if cur not in self.graph:
            await self.worker.producer(cur, self.queue_links, depth, is_source)

        else:
            await self.queue_links(cur, self.graph[cur], depth, is_source)

    def find_path(self, parents, dest):
        """
        Traces path from current node to parent.

        Args:
            parents:
            dest:

        Returns:
            path
        """
        path = [dest]
        while parents[dest] is not None:
            path.append(parents[dest])
            dest = parents[dest]

        return path

    async def queue_links(self, cur, resp, depth, is_source):
        """
        Adds node's children to to_visit queue for bfs.
        Callback that is fired after worker retrieves wiki_request.

        Args:
            cur:
            resp:
            depth:
            is_source:

        Returns:

        """
        if is_source:
            to_visit = self.to_visit_start
            came_from = self.came_from_start
        else:
            to_visit = self.to_visit_end
            came_from = self.came_from_end

        self.graph[cur] = resp
        for link in resp:
            if link in came_from:
                continue
            came_from[link] = cur
            await to_visit.put((link, depth + 1))
