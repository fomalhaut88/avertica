"""
This library contains asynchonous wrappers for the connection and cursor
objects in `vertica-python` library to interact with Vertica database.
It supports simple select queries yet, and there is no transactions,
commit and rollback asynchonous functionality.

Usage example:

    import avertica

    async with avertica.connect(**conn_info) as conn:
        async with conn.cursor() as cur:
            await cur.execute(query)
            rows = cur.fetchall()
"""

import asyncio

import vertica_python as ve

from .version import __version__


def connect(*args, **kwargs):
    """
    Creates an async connection object. Arguments are the same as in
    sync connection in `vertica-python`.
    """
    return AsyncConnection(*args, **kwargs)


class AsyncConnection:
    """
    An asynchonous wrapper over `vertica-python` connection. It supports
    `async with` and getting cursor object (that is an asynchonous wrapper
    as well).
    """
    def __init__(self, *args, **kwargs):
        self._conn = ve.connect(*args, **kwargs)

    def __del__(self):
        self.close()

    def close(self):
        """
        Closes the connection.
        """
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def cursor(self):
        """
        Creates an asynchonous cursor.
        """
        return AsyncCursor(self._conn)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self.close()


class AsyncCursor:
    def __init__(self, conn):
        self._conn = conn
        self._cursor = self._conn.cursor()

    def __del__(self):
        self.close()

    def close(self):
        """
        Closes the cursor.
        """
        if self._cursor is not None:
            self._cursor.close()
            self._cursor = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self.close()

    async def execute(self, *args):
        """
        Async execute function.
        """
        await _async_execute(self._cursor.execute, args)

    def fetchall(self):
        """
        Passes `fetchall`.
        """
        return self._cursor.fetchall()

    def fetchone(self):
        """
        Passes `fetchone`.
        """
        return self._cursor.fetchone()


def _async_execute(func, args):
    """
    A wrapper that transforms a sync function into an async one.
    It uses `loop.run_in_executor` inside with the default executor.
    Details: https://docs.python.org/3/library/asyncio-eventloop.html
    """
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(None, func, *args)
