PUPRemote documentation
=======================

Use this library to communicate from a pyboard like OpenMV or LMS-ESP32 
as a Powered UP (PUP) Device with LEGO smart hubs. 
It has a PUPRemote library that acts more like RPC (Remote Procedure Calling).
The library is compatible with Pybricks, SPIKE2, and Robot Inventor.

Example
-------
Run this on OpenMV

.. literalinclude:: ../examples/openmv_simple/main.py
    :language: python

Run this on Pybricks. Be sure to create a file called `pupremote.py` with
the contents of `pupremote.py<https://github.com/antonvh/PUPRemote/blob/main/src/pupremote.py>`_.

.. literalinclude:: ../examples/openmv_simple/pybricks_spike.py
    :language: python

API documentation
-----------------

.. automodule:: pupremote
    :members:

.. automodule:: lpf2
    :members: