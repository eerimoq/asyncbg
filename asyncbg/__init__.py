import asyncio
import concurrent.futures
import multiprocessing

from .version import __version__


def process_main(queue, callback, *args, **kwargs):
    try:
        result = callback(*args, **kwargs)
        exception = None
    except BaseException as e:
        result = None
        exception = e

    queue.put((result, exception))


def thread_main(callback, *args, **kwargs):
    queue = multiprocessing.Queue()
    proc = multiprocessing.Process(target=process_main,
                                   args=(queue, callback, *args),
                                   kwargs=kwargs)
    proc.start()
    result, exception = queue.get()
    proc.join()

    return result, exception


class Pool(concurrent.futures.ThreadPoolExecutor):
    """Same as ``concurrent.futures.ThreadPoolExecutor``, but with the
    ``call()`` method added.

    """

    async def call(self, callback, *args, **kwargs):
        """Call given callback with given arguments in another process in the
        worker pool when a worker is available.

        Returns the value returned by the callback, or raises the
        exceptions raised by the callback.

        Callback positional and keyword arguments can not be used for
        output, as the multiprocessing module does not support that.

        Call ``work()`` in a worker pool:

        >>> def work():
        >>>     pass
        >>>
        >>> pool = asyncbg.Pool()
        >>> asyncio.run(pool.call(work))

        """

        result, exception = await asyncio.wrap_future(
            self.submit(thread_main,
                        callback,
                        *args,
                        **kwargs))

        if exception is not None:
            raise exception

        return result


_DEFAULT_POOL = Pool()


async def call(callback, *args, **kwargs):
    """Call given callback with given arguments in another process.

    Returns the value returned by the callback, or raises the
    exceptions raised by the callback.

    Callback positional and keyword arguments can not be used for
    output, as the multiprocessing module does not support that.

    Call ``work()`` in another process:

    >>> def work():
    >>>     pass
    >>>
    >>> asyncio.run(asyncbg.call(work))

    """

    return await _DEFAULT_POOL.call(callback, *args, **kwargs)
