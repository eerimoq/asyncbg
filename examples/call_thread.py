import time
import asyncio
import asyncbg


def background_work():
    print('Background sleep for 5 seconds.')
    time.sleep(5)
    print('Background sleep done.')


async def foreground_work():
    for i in range(5):
        print('Foreground sleep for 1 second.')
        await asyncio.sleep(1)
        print('Foreground sleep done.')


async def main():
    await asyncio.gather(asyncbg.call_thread(background_work),
                         foreground_work())


asyncio.run(main())
