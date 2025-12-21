# Async demo for Pybricks hub using PUPRemoteHub
# Place src/pupremote_hub.py on the hub and run this.

from pybricks.parameters import Port
from pybricks.tools import multitask, run_task, wait
from pupremote_hub import PUPRemoteHub

# Initialize hub-side and mirror commands/channels defined on the sensor-side
p = PUPRemoteHub(Port.A)

# Mirror the sensor-side definitions
p.add_channel("cntr", to_hub_fmt="B")
p.add_command("msg", to_hub_fmt="repr", from_hub_fmt="repr")


async def hello():
    while True:
        # Call remote function 'msg' asynchronously
        result = await p.call_multitask("msg", "hello from hub")
        # Do something with the result (optional)
        print(result)
        await wait(500)

async def cntr():
    while True:
        # Call remote function 'cntr' asynchronously
        result = await p.call_multitask("cntr")
        # Do something with the result (optional)
        print(result)
        await wait(333)

async def main():
    # race=True ensures the program finishes when 
    # the first user thread is done.
    await multitask(p.process_calls(), hello(), cntr(), race=True)

run_task(main())
