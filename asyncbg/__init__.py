import asyncio
import concurrent.futures

from .version import __version__


class ProcessPoolExecutor(concurrent.futures.ProcessPoolExecutor):
    """Same as ``concurrent.futures.ProcessPoolExecutor``, but with the
    ``call()`` method added.

    """

    async def call(self, callback, *args, **kwargs):
        """Coroutine calling given callback with given arguments in a process
        in the worker pool.

        Returns the value returned by the callback, or raises the
        exceptions raised by the callback.

        Callback positional and keyword arguments can not be used for
        output, as the multiprocessing module does not support that.

        Call ``work()`` in a worker pool:

        >>> def work():
        >>>     pass
        >>>
        >>> pool = asyncbg.ProcessPoolExecutor()
        >>> asyncio.run(pool.call(work))

        """

        return await asyncio.wrap_future(self.submit(callback, *args, **kwargs))


_DEFAULT_POOL = ProcessPoolExecutor()


def call(callback, *args, **kwargs):
    """Coroutine calling given callback with given arguments in
    another process.

    Returns the value returned by the callback, or raises the
    exceptions raised by the callback.

    Callback positional and keyword arguments can not be used for
    output, as the multiprocessing module does not support that.

    Call ``work()`` in a worker process:

    >>> def work():
    >>>     pass
    >>>
    >>> asyncio.run(asyncbg.call(work))

    """

    return _DEFAULT_POOL.call(callback, *args, **kwargs)
