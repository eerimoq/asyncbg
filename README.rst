|buildstatus|_
|coverage|_

Asyncio background tasks
========================

Asyncio background tasks in Python 3.7 and later.

Run CPU intensive long running tasks without blocking the asyncio
loop.

Project homepage: https://github.com/eerimoq/asyncbg

Documentation: https://asyncbg.readthedocs.org/en/latest

Installation
============

.. code-block:: python

    pip install asyncbg

Examples
========

There are plenty of examples in the `examples folder`_.

Default worker
--------------

Run ``main()`` in the default worker thread.

.. code-block:: python

   import asyncio
   import asyncbg

   async def work():
       pass

   asyncio.run(asyncbg.run(work()))

Worker pool
-----------

Create a worker pool with two worker threads, and run three coroutines
in it (up to two coroutines in parallel).

.. code-block:: python

   import asyncio
   import asyncbg

   async def work():
       pass

   async def main():
       pool = asyncbg.WorkerPool()
       await asyncio.gather(pool.run(work()),
                            pool.run(work()),
                            pool.run(work()))

   asyncio.run(main())

.. |buildstatus| image:: https://travis-ci.org/eerimoq/asyncbg.svg?branch=master
.. _buildstatus: https://travis-ci.org/eerimoq/asyncbg

.. |coverage| image:: https://coveralls.io/repos/github/eerimoq/asyncbg/badge.svg?branch=master
.. _coverage: https://coveralls.io/github/eerimoq/asyncbg

.. _examples folder: https://github.com/eerimoq/asyncbg/tree/master/examples
