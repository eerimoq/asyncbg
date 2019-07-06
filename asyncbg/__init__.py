import threading
import asyncio

from .version import __version__


class Worker(threading.Thread):

    def __init__(self):
        super().__init__()
        self.loop = asyncio.new_event_loop()

    def run(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()


class WorkerPool:
    """The worker pool may only be used from a single asyncio loop. It is
    *not* thread safe.

    """

    def __init__(self, number_of_workers=4):
        self._workers = asyncio.Queue()

        for _ in range(number_of_workers):
            worker = Worker()
            worker.daemon = True
            worker.start()
            self._workers.put_nowait(worker)

    async def run(self, coro):
        """Run given coroutine in the worker pool when a worker is available.

        Returns the value returned by the coroutine, or raises the
        exceptions raised by the coroutine.

        """

        worker = await self._workers.get()

        try:
            result = await run(coro, worker)
        finally:
            await self._workers.put(worker)

        return result


# The default worker.
WORKER = Worker()
WORKER.daemon = True
WORKER.start()


async def _wrapper(coro, loop, queue):
    try:
        result = await coro
        exception = None
    except Exception as e:
        result = None
        exception = e

    asyncio.run_coroutine_threadsafe(queue.put((result, exception)), loop)


async def run(coro, worker=None):
    """Run given coroutine in given worker thread, or the default worker
    thread if no worker thread is given.

    Returns the value returned by the coroutine, or raises the
    exceptions raised by the coroutine.

    This functions is thread safe.

    """

    if worker is None:
        worker = WORKER

    queue = asyncio.Queue()
    wrapper = _wrapper(coro, asyncio.get_event_loop(), queue)
    asyncio.run_coroutine_threadsafe(wrapper, worker.loop)
    result, exception = await queue.get()

    if exception is not None:
        raise exception

    return result
