import time
import asyncio
import asyncbg


async def background_work():
    print('Background sleep for 3 seconds.')
    time.sleep(3)
    print('Background sleep done.')


async def foreground_work():
    for i in range(5):
        print('Foreground sleep for 1 second.')
        await asyncio.sleep(1)
        print('Foreground sleep done.')


async def main():
    pool = asyncbg.WorkerPool()
    await asyncio.gather(pool.run(background_work()),
                         pool.run(background_work()),
                         pool.run(background_work()),
                         pool.run(background_work()),
                         pool.run(background_work()),
                         foreground_work())


asyncio.run(main())
