# Trying to emulate a distance sensor
# Crash requires import machine;machine.reset()
# Definitions from https://github.com/maarten-pennings/Lego-Mindstorms/blob/main/ms4/faq.md#what-is-port-info-telling-me-about-modes

from lpf2 import LPF2, DATA16, ABSOLUTE, DATA8
from time import ticks_ms, time, sleep_ms
import struct

distance_sensor_modes = [
    {
        "symbol": "CM",
        "format": {"datasets": 1, "type": 1, "figures": 5, "decimals": 1},
        "capability": b"@\x00\x00\x00\x04\x84",
        "map_out": 0,
        "name": "DISTL",
        "pct": (0.0, 100.0),
        "map_in": 145,
        "si": (0.0, 250.0),
        "raw": (0.0, 2500.0),
    },
    {
        "symbol": "CM",
        "format": {"datasets": 1, "type": 1, "figures": 4, "decimals": 1},
        "capability": b"@\x00\x00\x00\x04\x84",
        "map_out": 0,
        "name": "DISTS",
        "pct": (0.0, 100.0),
        "map_in": 241,
        "si": (0.0, 32.0),
        "raw": (0.0, 320.0),
    },
    {
        "symbol": "CM",
        "format": {"datasets": 1, "type": 1, "figures": 5, "decimals": 1},
        "capability": b"@\x00\x00\x00\x04\x84",
        "map_out": 0,
        "name": "SINGL",
        "pct": (0.0, 100.0),
        "map_in": 144,
        "si": (0.0, 250.0),
        "raw": (0.0, 2500.0),
    },
    {
        "symbol": "ST",
        "format": {"datasets": 1, "type": 0, "figures": 1, "decimals": 0},
        "capability": b"@\x00\x00\x00\x04\x84",
        "map_out": 0,
        "name": "LISTN",
        "pct": (0.0, 100.0),
        "map_in": 16,
        "si": (0.0, 1.0),
        "raw": (0.0, 1.0),
    },
    {
        "symbol": "uS",
        "format": {"datasets": 1, "type": 2, "figures": 5, "decimals": 0},
        "capability": b"@\x00\x00\x00\x04\x84",
        "map_out": 0,
        "name": "TRAW",
        "pct": (0.0, 100.0),
        "map_in": 144,
        "si": (0.0, 14577.0),
        "raw": (0.0, 14577.0),
    },
    {
        "symbol": "PCT",
        "format": {"datasets": 4, "type": 0, "figures": 3, "decimals": 0},
        "capability": b"@ \x00\x00\x04\x84",
        "map_out": 16,
        "name": "LIGHT",
        "pct": (0.0, 100.0),
        "map_in": 0,
        "si": (0.0, 100.0),
        "raw": (0.0, 100.0),
    },
    {
        "symbol": "PCT",
        "format": {"datasets": 1, "type": 0, "figures": 1, "decimals": 0},
        "capability": b"@\x80\x00\x00\x04\x84",
        "map_out": 144,
        "name": "PING",
        "pct": (0.0, 100.0),
        "map_in": 0,
        "si": (0.0, 1.0),
        "raw": (0.0, 1.0),
    },
    {
        "symbol": "PCT",
        "format": {"datasets": 1, "type": 1, "figures": 4, "decimals": 0},
        "capability": b"@\x00\x00\x00\x04\x84",
        "map_out": 0,
        "name": "ADRAW",
        "pct": (0.0, 100.0),
        "map_in": 144,
        "si": (0.0, 1024.0),
        "raw": (0.0, 1024.0),
    },
    {
        "symbol": "PCT",
        "format": {"datasets": 7, "type": 0, "figures": 3, "decimals": 0},
        "capability": b"@@\x00\x00\x04\x84",
        "map_out": 0,
        "name": "CALIB",
        "pct": (0.0, 100.0),
        "map_in": 0,
        "si": (0.0, 255.0),
        "raw": (0.0, 255.0),
    },
]
dist_sensor_id = 62

light_sensor_modes = [
    {
        "symbol": "IDX",
        "format": {"datasets": 1, "type": 0, "figures": 2, "decimals": 0},
        "capability": b"@\x00\x00\x00\x04\x84",
        "map_out": 0,
        "name": "COLOR",
        "pct": (0.0, 100.0),
        "map_in": 228,
        "si": (0.0, 10.0),
        "raw": (0.0, 10.0),
    },
    {
        "symbol": "PCT",
        "format": {"datasets": 1, "type": 0, "figures": 3, "decimals": 0},
        "capability": b"@\x00\x00\x00\x04\x84",
        "map_out": 0,
        "name": "REFLT",
        "pct": (0.0, 100.0),
        "map_in": 48,
        "si": (0.0, 100.0),
        "raw": (0.0, 100.0),
    },
    {
        "symbol": "PCT",
        "format": {"datasets": 1, "type": 0, "figures": 3, "decimals": 0},
        "capability": b"@\x00\x00\x00\x04\x84",
        "map_out": 0,
        "name": "AMBI",
        "pct": (0.0, 100.0),
        "map_in": 48,
        "si": (0.0, 100.0),
        "raw": (0.0, 100.0),
    },
    {
        "symbol": "PCT",
        "format": {"datasets": 3, "type": 0, "figures": 3, "decimals": 0},
        "capability": b"@\x00\x00\x00\x05\x04",
        "map_out": 16,
        "name": "LIGHT",
        "pct": (0.0, 100.0),
        "map_in": 0,
        "si": (0.0, 100.0),
        "raw": (0.0, 100.0),
    },
    {
        "symbol": "RAW",
        "format": {"datasets": 2, "type": 1, "figures": 4, "decimals": 0},
        "capability": b"@\x00\x00\x00\x04\x84",
        "map_out": 0,
        "name": "RREFL",
        "pct": (0.0, 100.0),
        "map_in": 16,
        "si": (0.0, 1024.0),
        "raw": (0.0, 1024.0),
    },
    {
        "symbol": "RAW",
        "format": {"datasets": 4, "type": 1, "figures": 4, "decimals": 0},
        "capability": b"@\x00\x00\x00\x04\x84",
        "map_out": 0,
        "name": "RGB I",
        "pct": (0.0, 100.0),
        "map_in": 16,
        "si": (0.0, 1024.0),
        "raw": (0.0, 1024.0),
    },
    {
        "symbol": "RAW",
        "format": {"datasets": 3, "type": 1, "figures": 4, "decimals": 0},
        "capability": b"@\x00\x00\x00\x04\x84",
        "map_out": 0,
        "name": "HSV",
        "pct": (0.0, 100.0),
        "map_in": 16,
        "si": (0.0, 360.0),
        "raw": (0.0, 360.0),
    },
    {
        "symbol": "RAW",
        "format": {"datasets": 4, "type": 1, "figures": 4, "decimals": 0},
        "capability": b"@\x00\x00\x00\x04\x84",
        "map_out": 0,
        "name": "SHSV",
        "pct": (0.0, 100.0),
        "map_in": 16,
        "si": (0.0, 360.0),
        "raw": (0.0, 360.0),
    },
    {
        "symbol": "RAW",
        "format": {"datasets": 4, "type": 1, "figures": 4, "decimals": 0},
        "capability": b"@\x00\x00\x00\x04\x84",
        "map_out": 0,
        "name": "DEBUG",
        "pct": (0.0, 100.0),
        "map_in": 16,
        "si": (0.0, 65535.0),
        "raw": (0.0, 65535.0),
    },
    {
        "symbol": "",
        "format": {"datasets": 7, "type": 1, "figures": 5, "decimals": 0},
        "capability": b"@@\x00\x00\x04\x84",
        "map_out": 0,
        "name": "CALIB",
        "pct": (0.0, 100.0),
        "map_in": 0,
        "si": (0.0, 65535.0),
        "raw": (0.0, 65535.0),
    },
]
light_sensor_id = 61


def mode_convert(lms_modes):
    result = []
    for lms_mode in lms_modes:
        result.append(
            LPF2.mode(
                name=lms_mode["name"].encode("UTF-8")
                + b"\x00"
                + lms_mode["capability"],
                size=lms_mode["format"]["datasets"],
                data_type=lms_mode["format"]["type"],
                writable=1 if lms_mode["map_out"] else 0,
                format=f"{lms_mode['format']['figures']}.{lms_mode['format']['decimals']}",
                raw_range=lms_mode["raw"],
                percent_range=lms_mode["pct"],
                si_range=lms_mode["si"],
                symbol=lms_mode["symbol"],
                functionmap=[lms_mode["map_in"], lms_mode["map_out"]],
                view=True,
            )
        )
    return result


single_mode_ls = [
    LPF2.mode(
        "GAMEPAD",
        6,
        DATA16,
        format="5.0",
        symbol="XYBD",
        raw_range=(0.0, 512.0),
        percent_range=(0.0, 1024.0),
        si_range=(0.0, 512.0),
    )
]

single_mode_ds = [
    LPF2.mode(
        "DISTL",
        1,
        DATA16,
        format="5.1",
        symbol="CM",
        raw_range=(0.0, 250.0),
        percent_range=(0.0, 100.0),
        si_range=(0.0, 2500.0),
        functionmap=[0, 145],
    )
]

sensor_emu = LPF2(single_mode_ls, 61, debug=True) 

sensor_emu = LPF2(mode_convert(distance_sensor_modes), 62, debug=True) # Connects but no hearbeat.

sensor_emu = LPF2(
    single_mode_ds, 62, debug=True
)  


d = 0
while 1:
    d += 1
    sensor_emu.send_payload(struct.pack("h", d))
    data_in = sensor_emu.heartbeat()
    print(d)
    if data_in:
        print(f"\nReceived: {data_in[0]} on mode {data_in[1]}")
    sleep_ms(15)
