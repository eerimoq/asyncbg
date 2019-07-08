import asyncio
import asyncbg
import logging
import time


LOGGER = logging.getLogger(__name__)


def background_work():
    LOGGER.info('Worker 1!')
    time.sleep(1)
    LOGGER.info('Worker 2!')


logging.basicConfig(level=logging.INFO)
LOGGER.info('Main!')
asyncio.run(asyncbg.call(background_work))
