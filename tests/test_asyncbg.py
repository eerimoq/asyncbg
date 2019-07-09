import asyncio
import unittest

import asyncbg


def call_result_work():
    return 5


def call_exception_work():
    raise Exception()


def pool_work(value_1, value_2=1):
    return value_1 * value_2


class AsyncbgTest(unittest.TestCase):

    def test_call_result(self):
        asyncio.run(self.call_result())

    async def call_result(self):
        self.assertEqual(await asyncbg.call(call_result_work), 5)

    def test_call_exception(self):
        asyncio.run(self.call_exception())

    async def call_exception(self):
        with self.assertRaises(Exception):
            await asyncbg.call(call_exception_work)

    def test_pool(self):
        asyncio.run(self.pool())

    async def pool(self):
        pool = asyncbg.ProcessPoolExecutor()

        for i in range(10):
            self.assertEqual(await pool.call(pool_work, i, value_2=i), i * i)


if __name__ == '__main__':
    unittest.main()
