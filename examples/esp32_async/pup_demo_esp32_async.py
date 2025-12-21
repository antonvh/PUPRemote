# Async demo for LMS-ESP32 using PUPRemoteSensor
# Copy this file to the LMS-ESP32 as main.py and reboot.

import asyncio
from pupremote import PUPRemoteSensor

# Example callback function callable from the hub
# Register this on the sensor side so the hub can call it.
async def msg(*argv):
    # Echo the arguments or return a demo string
    return argv if argv else "demo"


async def main():
    # Initialize sensor-side with async support and a simple channel
    p = PUPRemoteSensor(power=True)
    p.add_channel("cntr", to_hub_fmt="B")
    p.add_command("msg", to_hub_fmt="repr", from_hub_fmt="repr")

    # Run heartbeat and callback processing concurrently
    asyncio.create_task(p.process_async())

    # Periodically update a channel for the hub to read
    cnt = 0
    while True:
        cnt = (cnt + 1) % 255
        p.update_channel("cntr", cnt)
        await asyncio.sleep_ms(500)


# Run the async main
try:
    asyncio.run(main())
finally:
    # clean up
    asyncio.new_event_loop()