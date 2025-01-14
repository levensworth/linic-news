from __future__ import annotations

import logging
import typing
from contextlib import asynccontextmanager, contextmanager
from typing import AsyncIterator, Generator, Type, TypeVar, overload

from psycopg import AsyncConnection, Connection
from psycopg.rows import class_row
from psycopg_pool import AsyncConnectionPool, ConnectionPool

# from src.core.config import Environment, settings


_T = TypeVar("_T")


class Database:
    """Database abstraction layer which
    handles the session management as well as database connection.
    """

    def __init__(self, db_url: str, dev: bool = False) -> None:
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__dev = dev

        self.__connection_pool = ConnectionPool(
            conninfo=db_url,
            timeout=60 * 5,
            reconnect_timeout=60 * 60,
            open=(
                False if self.__dev else True
            ),  # do not starts the connection pool immediately if test environment.
        )

        self.__async_connection_pool = AsyncConnectionPool(
            conninfo=db_url,
            timeout=60 * 5,
            reconnect_timeout=60 * 60,
            open=False,
            min_size=8,
        )

    @overload
    @contextmanager
    def get_session(self, t: None) -> Generator[Connection[typing.Any], None, None]: ...

    @overload
    @contextmanager
    def get_session(self, t: Type[_T]) -> Generator[Connection[_T], None, None]: ...

    @contextmanager
    def get_session(
        self, t: Type[_T] | None
    ) -> Generator[Connection[_T] | Connection[typing.Any], None, None]:
        # checks for an open connection, if not then opens the connection pool
        if not self.__connection_pool._opened:
            self.__connection_pool.open()

        self.__connection_pool.check()

        session = self.__connection_pool.getconn()

        try:
            session.row_factory = class_row(t) if t is not None else session.row_factory  # type: ignore
            yield session
        except Exception as e:
            self.__logger.exception("Session rollback because of exception")
            session.rollback()
            raise e
        finally:
            # return used connection
            self.__connection_pool.putconn(session)

    @overload
    @asynccontextmanager
    def aget_session(self, t: Type[_T]) -> AsyncIterator[AsyncConnection[_T]]: ...

    @overload
    @asynccontextmanager
    def aget_session(self, t: None) -> AsyncIterator[AsyncConnection[typing.Any]]: ...

    @asynccontextmanager
    async def aget_session(
        self, t: Type[_T] | None
    ) -> AsyncIterator[AsyncConnection[_T] | AsyncConnection[typing.Any]]:
        # checks for an open connection, if not then opens the connection pool
        if not self.__async_connection_pool._opened:
            await self.__async_connection_pool.open(wait=True)

        await self.__async_connection_pool.check()

        async with self.__async_connection_pool.connection() as session:
            try:
                session.row_factory = (
                    class_row(t) if t is not None else session.row_factory  # type: ignore
                )
                if t is None:
                    yield session
                else:
                    yield typing.cast(AsyncConnection[_T], session)

            except Exception as e:
                self.__logger.exception("Session rollback because of exception")
                await session.rollback()
                raise e
