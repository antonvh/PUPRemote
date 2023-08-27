#!/bin/micropython
from time import ticks_ms
data = bytes('"hello world"', "utf-8")
padding = 32-len(data)
data += bytes(padding)

# Test different strip methods
# Not all micropython ports support rstrip on bytes

start = ticks_ms()
for i in range(100000):
    stripped = data.rstrip(b"\x00")
print("rstrip", ticks_ms()-start)

start = ticks_ms()
for i in range(100000):
    j = 31
    while data[j] == 0 and j > 0:
        j -= 1
    stripped = data[:j+1]
print("while", ticks_ms()-start)

start = ticks_ms()
for i in range(100000):
    str_data = data.decode("UTF-8").rstrip("\x00")
    if str_data:
        retval = (eval(str_data),)
    else:
        # Probably nothing left after stripping zero's
        retval = ("",)
print("decode & eval", ticks_ms()-start)

start = ticks_ms()
for i in range(100000):
    j = 31
    while data[j] == 0 and j > 0:
        j -= 1
    if j > 0:
        retval = (eval(data[:j+1]),)
    else:
        # Probably nothing left after stripping zero's
        retval = ("",)
print("while & eval", ticks_ms()-start)

start = ticks_ms()
for i in range(100000):
    str_data = data.rstrip(b"\x00")
    if str_data:
        retval = (eval(str_data),)
    else:
        # Probably nothing left after stripping zero's
        retval = ("",)
print("rstrip bytes & eval", ticks_ms()-start)

start = ticks_ms()
for i in range(100000):
    str_data = bytes( (c for c in data if c != 0) )
    if str_data:
        retval = (eval(str_data),)
    else:
        # Probably nothing left after stripping zero's
        retval = ("",)
print("list comp & eval", ticks_ms()-start)