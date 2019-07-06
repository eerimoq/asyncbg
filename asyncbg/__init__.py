import asyncio
import concurrent.futures

from .version import __version__


class ThreadPoolExecutor(concurrent.futures.ThreadPoolExecutor):
    """Same as ``concurrent.futures.ThreadPoolExecutor``, but with the
    ``call()`` method added.

    """

    async def call(self, callback, *args, **kwargs):
        """Call given callback with given arguments in the worker pool when a
        worker is available.

        Returns the value returned by the callback, or raises the
        exceptions raised by the callback.

        Call ``work()`` in a worker pool:

        >>> def work():
        >>>     pass
        >>>
        >>> pool = asyncbg.ThreadPoolExecutor()
        >>> asyncio.run(pool.call(work))

        """

        return await asyncio.wrap_future(self.submit(callback, *args, **kwargs))


_DEFAULT_POOL = ThreadPoolExecutor()


async def call(callback, *args, **kwargs):
    """Call given callback with given arguments in a worker thread.

    Returns the value returned by the callback, or raises the
    exceptions raised by the callback.

    Call ``work()`` in a worker thread:

    >>> def work():
    >>>     pass
    >>>
    >>> asyncio.run(asyncbg.call(work))

    """

    return await _DEFAULT_POOL.call(callback, *args, **kwargs)
