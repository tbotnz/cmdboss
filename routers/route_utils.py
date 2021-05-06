import logging

from fastapi import HTTPException

from backend.util.exceptions import (
    CMDBOSSHTTPException
)

from contextlib import contextmanager
import asyncio
from functools import wraps

from backend.models.system import ResponseBasic

log = logging.getLogger(__name__)


class SyncAsyncDecoratorFactory:
    """Courtesy of StackOverflow & Github user https://gist.github.com/anatoly-kussul
    https://gist.github.com/anatoly-kussul/f2d7444443399e51e2f83a76f112364d/ff1f94b1bd07741ce209cc61832f920adb49aedf"""

    @contextmanager
    def wrapper(self, func, *args, **kwargs):
        yield

    def __call__(self, func):
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            with self.wrapper(func, *args, **kwargs):
                return func(*args, **kwargs)

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            with self.wrapper(func, *args, **kwargs):
                return await func(*args, **kwargs)

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper


class HttpErrorHandler(SyncAsyncDecoratorFactory):
    @contextmanager
    def wrapper(self, *args, **kwargs):
        try:
            yield
        except asyncio.CancelledError:
            raise
        except Exception as e:
            import traceback
            log.exception(f"CMDBOSSHTTPException Log: {e}")
            error = traceback.format_exc().splitlines()
            raise CMDBOSSHTTPException(status_code=500, result=error)
