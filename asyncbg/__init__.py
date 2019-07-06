import threading
from queue import Queue
import asyncio

from .version import __version__


class Worker(threading.Thread):

    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        
    def run(self):
        while True:
            callback, loop, queue = self.queue.get()

            try:
                result = callback()
                exception = None
            except Exception as e:
                result = None
                exception = e

            asyncio.run_coroutine_threadsafe(queue.put((result, exception)),
                                             loop)


def create_worker():
    worker = Worker(Queue())
    worker.daemon = True
    worker.start()

    return worker


class WorkerPool:
    """The worker pool may only be used from a single asyncio loop. It is
    *not* thread safe.

    """

    def __init__(self, number_of_workers=4):
        self._workers = asyncio.Queue()

        for _ in range(number_of_workers):
            self._workers.put_nowait(create_worker())

    async def call(self, callback):
        """Call given callback in the worker pool when a worker is available.

        Returns the value returned by the callback, or raises the
        exceptions raised by the coroutine.

        Run ``work()`` in a worker pool:

        >>> def work():
        >>>     pass
        >>>
        >>> pool = asyncbg.WorkerPool()
        >>> asyncio.run(pool.call(work))

        """

        worker = await self._workers.get()

        try:
            result = await call(callback, worker)
        finally:
            await self._workers.put(worker)

        return result


_DEFAULT_WORKER = create_worker()


async def call(callback, worker=None):
    """Call given callback in given worker thread, or the default worker
    thread if no worker thread is given.

    Returns the value returned by the callback, or raises the
    exceptions raised by the callback.

    This functions is thread safe.

    Run ``work()`` in the default worker thread:

    >>> async def work():
    >>>     pass
    >>>
    >>> asyncio.run(asyncbg.call(work()))

    """

    if worker is None:
        worker = _DEFAULT_WORKER

    queue = asyncio.Queue()
    worker.queue.put((callback, asyncio.get_event_loop(), queue))
    result, exception = await queue.get()

    if exception is not None:
        raise exception

    return result
