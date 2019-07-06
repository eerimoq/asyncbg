import asyncio
import unittest

import asyncbg


class AsyncbgTest(unittest.TestCase):

    def test_run_result(self):
        asyncio.run(self.run_result())

    async def run_result(self):
        async def main():
            return 5

        self.assertEqual(await asyncbg.run(main()), 5)

    def test_run_exception(self):
        asyncio.run(self.run_exception())

    async def run_exception(self):
        async def main():
            raise Exception()

        with self.assertRaises(Exception):
            await asyncbg.run(main())


if __name__ == '__main__':
    unittest.main()
