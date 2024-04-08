PUPRemote documentation
=======================

Use this library to communicate from a pyboard like OpenMV or LMS-ESP32 
as a Powered UP (PUP) Device with LEGO smart hubs. 
It has a PUPRemote library that acts more like RPC (Remote Procedure Calling).
The library is compatible with Pybricks, SPIKE2, and Robot Inventor.

`pupremote.py` works on all platforms, also on Pybricks. However, for Pybricks, there 
is also a smaller file, called `pupremote_hub.py` that only contains the `PUPRemoteHub` class.
So on Pybricks, we suggest using `from pupremote_hub import PUPRemoteHub`

Example
-------
Run this on OpenMV

.. literalinclude:: ../examples/openmv_simple/main.py
    :language: python

Run this on Pybricks. Be sure to create a file called `pupremote.py` with
the contents of `pupremote.py <https://github.com/antonvh/PUPRemote/blob/main/src/pupremote.py>`_.

.. literalinclude:: ../examples/openmv_simple/pybricks_spike.py
    :language: python

PUPRemote API documentation
---------------------------

.. automodule:: pupremote
    :members:

.. automodule:: lpf2
    :members:


BluePad API documentation
-------------------------

This is a small wrapper library to use with the `BluePad32 LPF2 for Pybricks firmware <https://firmware.antonsmindstorms.com/>`_. It uses the PUPRemote library to communicate with the firmware of the LMS-ESP32 acting like
a Lego sensor and supporting reading the gamepad and driving NeoPixels and Servo's that are connected to the LMS-ESP32 board. 
This firmware is based on the nice `Bluepad32 for Arduino <https://github.com/ricardoquesada/bluepad32/blob/main/docs/plat_arduino.md>`_ library made by Ricardo Quesada.

.. automodule:: bluepad
    :members:
