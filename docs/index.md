# PUPRemote

Communicate with LEGO® Powered Up hubs from a hub extension board like lms-esp32, or any other MCU running micropython.

---

## Installation

### LMS-ESP32 running micropython

- In pybricks use the 'Import file' button (above the file list) to import `pupremote_hub.py`. In your program do this: `from pupremote_hub import PUPRemoteHub`. This is a minimized version of pupremote.py for hubs with little memory.
- Alternatively import `pupremote.py`, and in your program do this: `from pupremote import PUPRemoteHub`.
- Flash your lms-esp32 with [the latest micropython firmware from Anton's Mindstorms](https://firmware.antonsmindstorms.com). No need to copy libraries, they come with the firmware.

### LMS-ESP32 running bluepad

- Alternatively import `bluepad.py`, and use the `pybricks_blocks_boilerplate.py` in Pybricks blocks.
- Flash your lms-esp32 with [the latest BluePad firmware from Anton's Mindstorms](https://firmware.antonsmindstorms.com). No need to copy libraries, they come with the firmware.
