import asyncio
import unittest
from functools import partial

import asyncbg


class AsyncbgTest(unittest.TestCase):

    def test_call_result(self):
        asyncio.run(self.call_result())

    async def call_result(self):
        def work():
            return 5

        self.assertEqual(await asyncbg.call(work), 5)

    def test_call_exception(self):
        asyncio.run(self.call_exception())

    async def call_exception(self):
        def work():
            raise Exception()

        with self.assertRaises(Exception):
            await asyncbg.call(work)

    def test_worker_pool(self):
        asyncio.run(self.worker_pool())

    async def worker_pool(self):
        pool = asyncbg.WorkerPool()

        def work(value):
            return value

        for i in range(10):
            self.assertEqual(await pool.call(partial(work, i)), i)


if __name__ == '__main__':
    unittest.main()
