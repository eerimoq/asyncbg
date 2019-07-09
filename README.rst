|buildstatus|_
|coverage|_

Asyncio background tasks
========================

Asyncio background tasks in Python 3.7 and later.

Run CPU intensive long running tasks without blocking the asyncio
loop, implemented as a lightweight asyncio layer on top of the
multiprocessing module.

Project homepage: https://github.com/eerimoq/asyncbg

Documentation: https://asyncbg.readthedocs.org/en/latest

Installation
============

.. code-block:: python

   pip install asyncbg

Examples
========

There are more examples in the `examples folder`_.

Call
----

Call ``work(a, b)`` in another process. The script output is ``Result: 9``.

.. code-block:: python

   import asyncio
   import asyncbg

   def work(a, b):
       return a + b

   async def main():
       result = await asyncbg.call(work, 4, 5)
       print(f'Result: {result}')

   asyncio.run(main())

Process pool
------------

Create a process pool with two workers, and call ``work()`` three
times in it (up to two callbacks called in parallel).

.. code-block:: python

   import asyncio
   import asyncbg

   def work():
       pass

   async def main():
       pool = asyncbg.ProcessPoolExecutor(max_workers=2)
       await asyncio.gather(pool.call(work),
                            pool.call(work),
                            pool.call(work))

   asyncio.run(main())

.. |buildstatus| image:: https://travis-ci.org/eerimoq/asyncbg.svg?branch=master
.. _buildstatus: https://travis-ci.org/eerimoq/asyncbg

.. |coverage| image:: https://coveralls.io/repos/github/eerimoq/asyncbg/badge.svg?branch=master
.. _coverage: https://coveralls.io/github/eerimoq/asyncbg

.. _examples folder: https://github.com/eerimoq/asyncbg/tree/master/examples
