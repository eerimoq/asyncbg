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


# The default worker.
WORKER = Worker()
WORKER.daemon = True
WORKER.start()


async def _resume(future, queue):
    try:
        result = future.result()
        exception = None
    except Exception as e:
        result = None
        exception = e

    await queue.put((result, exception))


async def run(coro):
    """Run given coroutine in the background thread. Returns the value
    returned by the coroutine, or raises the exceptions raised by the
    coroutine.

    """

    future = asyncio.run_coroutine_threadsafe(coro, WORKER.loop)
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue()

    def on_done(future):
        asyncio.run_coroutine_threadsafe(_resume(future, queue), loop).result()

    future.add_done_callback(on_done)

    result, exception = await queue.get()

    if exception is not None:
        raise exception

    return result
