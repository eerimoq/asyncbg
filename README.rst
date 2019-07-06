|buildstatus|_
|coverage|_

Asyncio background tasks
========================

Asyncio background tasks in Python 3.7 and later.

Project homepage: https://github.com/eerimoq/asyncbg

Documentation: https://asyncbg.readthedocs.org/en/latest

Installation
============

.. code-block:: python

    pip install asyncbg

Examples
========

There are plenty of examples in the `examples folder`_.

Run
---

.. code-block:: python

   import time
   import asyncio
   import asyncbg


   async def background_main():
       print('Background sleep for 5 seconds.')
       time.sleep(5)
       print('Background sleep done.')


   async def foreground_main():
       for i in range(5):
           print('Foreground sleep for 1 second.')
           await asyncio.sleep(1)
           print('Foreground sleep done.')


   async def main():
       await asyncio.gather(asyncbg.run(background_main()),
                            foreground_main())


   asyncio.run(main())

.. |buildstatus| image:: https://travis-ci.org/eerimoq/asyncbg.svg?branch=master
.. _buildstatus: https://travis-ci.org/eerimoq/asyncbg

.. |coverage| image:: https://coveralls.io/repos/github/eerimoq/asyncbg/badge.svg?branch=master
.. _coverage: https://coveralls.io/github/eerimoq/asyncbg

.. _examples folder: https://github.com/eerimoq/asyncbg/tree/master/examples
