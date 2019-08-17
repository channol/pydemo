#!/usr/bin/python3
import time,sys,os,re
import asyncio

now= lambda : time.time()

async def capture(timeout):
    print(now())
    os.system('tshark -i any -a duration:{} -w /tmp/{}.pcap'.format(timeout,timeout))
    await asyncio.sleep(1)


start=now()
#coroutine = capture1()
#print(coroutine)
loop = asyncio.get_event_loop()
#task = loop.create_task(capture1())
#tasks = [asyncio.Task(capture()),asyncio.Task(capture1())]
tasks = [asyncio.ensure_future(capture(5)),asyncio.ensure_future(capture(10))]
print(tasks)
loop.run_until_complete(asyncio.wait(tasks))
#loop.run_until_complete(coroutine)

print('time:',now()-start)
