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

There are more examples in the `examples folder`_.

Call
----

Call ``work()`` in another process.

.. code-block:: python

   import asyncio
   import asyncbg

   def work():
       pass

   asyncio.run(asyncbg.call(work))

Pool
----

Create a pool with two workers, and call ``work()`` three times in it
(up to two callbacks called in parallel).

.. code-block:: python

   import asyncio
   import asyncbg

   def work():
       pass

   async def main():
       pool = asyncbg.Pool(max_workers=2)
       await asyncio.gather(pool.call(work),
                            pool.call(work),
                            pool.call(work))

   asyncio.run(main())

.. |buildstatus| image:: https://travis-ci.org/eerimoq/asyncbg.svg?branch=master
.. _buildstatus: https://travis-ci.org/eerimoq/asyncbg

.. |coverage| image:: https://coveralls.io/repos/github/eerimoq/asyncbg/badge.svg?branch=master
.. _coverage: https://coveralls.io/github/eerimoq/asyncbg

.. _examples folder: https://github.com/eerimoq/asyncbg/tree/master/examples
