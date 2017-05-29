#!/usr/bin/env python

"""
simple async example derived from python docs.

Will only work on Python 3.5 and above
"""

import time
import asyncio
import datetime
import random

# using "async" makes this a coroutine:
async def display_date(num):
    # the event loop has a time() built in.
    end_time = time.time() + 15.0  # we want it to run for 50 seconds.
    print("should end at:", end_time)
    while True:  # keep doing this until break
        print("instance: {} Time: {}".format(num, datetime.datetime.now()))
        print("current time:", time.time())
        if (time.time()) >= end_time:
            print("instance: {} is all done".format(num))
            break
        await asyncio.sleep(random.randint(0, 5))

# async def display_date(num, loop):
#     end_time = loop.time() + 50.0
#     while True:
#         print("Loop: {} Time: {}".format(num, datetime.datetime.now()))
#         if (loop.time() + 1.0) >= end_time:
#             break
#         await asyncio.sleep(random.randint(0, 5))


loop = asyncio.get_event_loop()

asyncio.ensure_future(display_date(1))
asyncio.ensure_future(display_date(2))


# asyncio.ensure_future(display_date(1, loop))
# asyncio.ensure_future(display_date(2, loop))
#loop.run_until_complete()
loop.run_forever()
