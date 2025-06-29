__author__ = "Anton Vanhoucke & Ste7an"
__copyright__ = "Copyright 2023,2024 AntonsMindstorms.com"
__license__ = "GPL"
__version__ = "2.1"
__status__ = "Production"

try:
    from pybricks.iodevices import PUPDevice
    from pybricks.tools import wait, run_task
    import ustruct as struct

    side = "Hub"
except ImportError:
    # We surely aren't on pybricks. Probably on the sensor side (openmv or lms-esp32)
    side = "Sensor"

    # Avoid errors when using Pybricks classes and functions.
    class PUPDevice:
        def __init__(self, port):
            pass

        def read(self, mode):
            pass

        def write(self, mode, data):
            pass

    def wait(ms):
        pass

    # Import modules for sensor side only.
    import asyncio
    import lpf2
    import struct
    from collections import deque

try:
    from micropython import const
except ImportError:
    # Create quick polyfill on platforms that don't support it
    def const(x):
        return x


MAX_PKT = const(16)
MAX_COMMANDS = const(16)
MAX_COMMAND_QUEUE_LENGTH = const(10)

# Dictionary keys
NAME = const(0)
SIZE = const(1)
TO_HUB_FORMAT = const(2)
FROM_HUB_FORMAT = const(3)
CALLABLE = const(4)
ARGS_TO_HUB = const(5)
ARGS_FROM_HUB = const(6)

#: WeDo Ultrasonic sensor id
WEDO_ULTRASONIC = const(35)
#: SPIKE Color sensor id
SPIKE_COLOR = const(61)
#: SPIKE Ultrasonic sensor id
SPIKE_ULTRASONIC = const(62)

CALLBACK = const(0)
CHANNEL = const(1)


class PUPRemote:
    """
    Base class for PUPRemoteHub and PUPRemoteSensor. Defines a list of commands
    and their formats. Contains encoding/decoding functions.
    """

    def __init__(self, max_packet_size=MAX_PKT):
        """
        :param max_packet_size: Set to 16 for Pybricks compatibility, defaults to 32.
        :type max_packet_size: int
        """
        # Store commands, size and format
        self.commands = []
        # Store mode names (commands) to look up their index
        self.modes = {}
        # Optional override for max packet size for Pybricks compatibility
        self.max_packet_size = max_packet_size

    def add_channel(self, mode_name: str, to_hub_fmt: str = ""):
        """
        Define a data channel to read on the hub. Use this function with identical parameters on both
        the sensor and the hub. You can call a channel like a command, but to update the data
        on the sensor side, you need to `update_channel(<name>, *args)`.

        :param mode_name: The name of the mode you defined on the sensor side.
        :type mode_name: str
        :param to_hub_fmt: The format string of the data sent from the sensor
            to the hub. Use 'repr' to receive any python object. Or use a struct format string,
            to receive a fixed size payload. See https://docs.python.org/3/library/struct.html

        :type to_hub_fmt: str
        """
        self.add_command(mode_name, to_hub_fmt=to_hub_fmt, command_type=CHANNEL)

    def add_command(
        self,
        mode_name: str,
        to_hub_fmt: str = "",
        from_hub_fmt: str = "",
        command_type=CALLBACK,
    ):
        """Define a remote call. Use this function with identical parameters on both
        the sensor and the hub.

        :param mode_name: The name of the mode you defined on the sensor side.
        :type mode_name: str
        :param to_hub_fmt: The format string of the data sent from the sensor
            to the hub. Use 'repr' to receive any python object. Or use a struct format string,
            to receive a fixed size payload. See https://docs.python.org/3/library/struct.html

        :type to_hub_fmt: str
        :param from_hub_fmt: The format string of the data sent from the hub
        :type from_hub_fmt: str

        """
        if to_hub_fmt == "repr" or from_hub_fmt == "repr":
            msg_size = self.max_packet_size
            num_args_from_hub = -1
            num_args_to_hub = -1
        else:
            size_to_hub_fmt = struct.calcsize(to_hub_fmt)
            size_from_hub_fmt = struct.calcsize(from_hub_fmt)
            msg_size = max(size_to_hub_fmt, size_from_hub_fmt)
            num_args_to_hub = len(
                struct.unpack(to_hub_fmt, bytearray(struct.calcsize(to_hub_fmt)))
            )
            num_args_from_hub = len(
                struct.unpack(from_hub_fmt, bytearray(struct.calcsize(from_hub_fmt)))
            )

        assert len(self.commands) < MAX_COMMANDS, "Command limit exceeded"
        assert msg_size <= self.max_packet_size, "Payload exceeds maximum packet size"
        self.commands.append(
            {
                NAME: mode_name,
                TO_HUB_FORMAT: to_hub_fmt,
                SIZE: msg_size,
                ARGS_TO_HUB: num_args_to_hub,
            }
        )
        if command_type == CALLBACK:
            self.commands[-1][FROM_HUB_FORMAT] = from_hub_fmt
            self.commands[-1][ARGS_FROM_HUB] = num_args_from_hub

        # Build a dictionary of mode names and their index
        self.modes[mode_name] = len(self.commands) - 1

    def decode(self, fmt: str, data: bytes):
        if fmt == "repr":
            # Remove trailing zero's (b'\x00') and eval the string
            clean = bytearray([c for c in data if c != 0])
            if clean:
                return (eval(clean),)
            else:
                # Probably nothing left after stripping zero's
                return ("",)
        else:
            size = struct.calcsize(fmt)
            data = struct.unpack(fmt, data[:size])
        return data

    def encode(self, size, format, *argv):
        if format == "repr":
            s = bytes(repr(*argv), "UTF-8")
        else:
            s = struct.pack(format, *argv)
        assert len(s) <= size, "Payload exceeds maximum packet size"
        return s


class PUPRemoteSensor(PUPRemote):
    """
    Class to communicate with a PUPRemoteHub. Use this class on the sensor side,
    on any board that runs MicroPython. You can enable 8V power on the M+ wire,
    so the buck converter on the SPIKE-OPENMV or LMS-ESP32 board side can supply high
    currents (op to 1700mA) to your appliances.

    :param sensor_id: The id of the sensor of the sensor to emulate, defaults to 62.
    :type sensor_id: int
    :param power: Set to True if the PUPRemoteHub needs 8V power on M+ wire, defaults to False.
    :type power: bool
    :param platform: Set to ESP32 or OPENMV, defaults to ESP32.
    :type platform: int
    :param max_packet_size: Set to max 32 bytes of payload, defaults to 16 for Pybricks compatibility.
    :type max_packet_size: int
    """

    def __init__(
        self,
        sensor_id=SPIKE_ULTRASONIC,
        power=False,
        max_packet_size=MAX_PKT,
        **kwargs,  # backward compatibility
    ):
        super().__init__(max_packet_size)
        self.connected = False
        self.power = power  ## ?
        self.mode_names = []  ## ?
        self.max_packet_size = max_packet_size
        self.lpup = lpf2.LPF2([], sensor_id=sensor_id, max_packet_size=max_packet_size)
        self._callback_queue = deque((), MAX_COMMAND_QUEUE_LENGTH)
        self._callback_lock = asyncio.Lock()

    def add_command(
        self,
        mode_name: str,
        to_hub_fmt: str = "",
        from_hub_fmt: str = "",
        command_type=CALLBACK,
    ):
        super().add_command(mode_name, to_hub_fmt, from_hub_fmt, command_type)
        writeable = 0
        if command_type == CALLBACK:
            self.commands[-1][CALLABLE] = eval(mode_name)
        if from_hub_fmt != "":
            writeable = lpf2.ABSOLUTE
        max_mode_name_len = 5 if self.power else 11
        assert (
            len(mode_name) <= max_mode_name_len
        ), "Name length must be <= {} with power={}".format(
            max_mode_name_len, self.power
        )
        if self.power:
            mode_name = (
                mode_name.encode("ascii")
                + b" " * (5 - len(mode_name))
                + b"\x00\x80\x00\x00\x00\x05\x04"
            )
        self.lpup.modes.append(
            self.lpup.mode(
                mode_name,
                self.commands[-1][SIZE],  # Size of the last command we added.
                lpf2.DATA8,
                writeable,
            )
        )

    async def _heartbeat_loop(self, interval_ms: int):
        """Continuously call heartbeat at fixed interval and enqueue callbacks"""
        while True:
            data = self.lpup.heartbeat()
            if data:
                async with self._callback_lock:
                    self._callback_queue.append(data)
            await asyncio.sleep(interval_ms / 1000)

    async def _process_callbacks(self):
        """Process incoming callbacks from queue serially"""
        while True:
            await asyncio.sleep(0)  # Yield to allow _heartbeat_loop to enqueue
            async with self._callback_lock:
                if self._callback_queue:
                    pl, mode = self._callback_queue.popleft()
                else:
                    continue

            if CALLABLE in self.commands[mode]:
                result = None
                args = self.decode(self.commands[mode][FROM_HUB_FORMAT], pl)
                result = await self.commands[mode][CALLABLE](*args)
                num_args = self.commands[mode][ARGS_TO_HUB]

                if result is None:
                    assert num_args <= 0, "{}() did not return value(s)".format(
                        self.commands[mode][NAME]
                    )
                else:
                    if not isinstance(result, tuple):
                        result = (result,)
                    if num_args >= 0:
                        assert num_args == len(
                            result
                        ), "{}() returned {} value(s) instead of expected {}".format(
                            self.commands[mode][NAME], len(result), num_args
                        )
                    pl = self.encode(
                        self.commands[mode][SIZE],
                        self.commands[mode][TO_HUB_FORMAT],
                        *result,
                    )
                    self.lpup.send_payload(pl, mode)

    async def process_async(self, interval_ms: int = 50):
        """Start both heartbeat and callback processing tasks."""
        # heartbeat at least 15 Hz (66ms)
        hb_task = asyncio.create_task(self._heartbeat_loop(interval_ms))
        cb_task = asyncio.create_task(self._process_callbacks())
        await asyncio.gather(hb_task, cb_task)

    def process(self):
        """
        Process the commands. Call this function in your main loop, preferably at least once every 20ms.
        It will handle the communication with the LEGO Hub, connect to it if needed,
        and call the registered commands.

        :return: True if connected to the hub, False otherwise.
        """
        data = self.lpup.heartbeat()
        if data is not None:
            pl, mode = data
            if CALLABLE in self.commands[mode]:
                result = None
                args = self.decode(self.commands[mode][FROM_HUB_FORMAT], pl)
                result = self.commands[mode][CALLABLE](*args)
                num_args = self.commands[mode][ARGS_TO_HUB]

                if result is None:
                    assert num_args <= 0, "{}() did not return value(s)".format(
                        self.commands[mode][NAME]
                    )
                else:
                    if not isinstance(result, tuple):
                        result = (result,)
                    if num_args >= 0:
                        assert num_args == len(
                            result
                        ), "{}() returned {} value(s) instead of expected {}".format(
                            self.commands[mode][NAME], len(result), num_args
                        )
                    pl = self.encode(
                        self.commands[mode][SIZE],
                        self.commands[mode][TO_HUB_FORMAT],
                        *result,
                    )
                    self.lpup.send_payload(pl, mode)
        return self.lpup.connected

    def update_channel(self, mode_name: str, *argv):
        """Update values in 'sensor' memory, so the hub can retrieve them with call().
        This is simpler than defining a function that is called remotely from the hub.

        :param mode_name: mode name you defined when you used `add_channel()`
        :type mode_name: str
        """
        mode = self.modes[mode_name]

        pl = self.encode(
            self.commands[mode][SIZE], self.commands[mode][TO_HUB_FORMAT], *argv
        )
        self.lpup.load_payload(pl, mode)

    async def update_channel_async(self, mode_name: str, *args):
        await asyncio.get_running_loop().run_in_executor(
            None, self.update_channel, mode_name, *args
        )


class PUPRemoteHub(PUPRemote):
    """
    Class to communicate with a PUPRemoteSensor. Use this class on the hub side,
    on any hub that runs Pybricks. Copy the commands you defined on the sensor side
    to the hub side.

    :param port: The port to which the PUPRemoteSensor is connected.
    :type port: Port (Example: Port.A)
    :param max_packet_size: Set to 16 for Pybricks compatibility, defaults to 32.
    :type max_packet_size: int
    """

    def _int8_to_uint8(self, arr):
        return [((i + 128) & 0xFF) - 128 for i in arr]

    def __init__(self, port, max_packet_size=MAX_PKT):
        super().__init__(max_packet_size)
        self.port = port
        try:
            self.pup_device = PUPDevice(port)
        except OSError:
            self.pup_device = None
            print("Check wiring and remote script. Unable to connect on ", self.port)
            raise
        # Multitask stuff
        self._queue = []
        self._multitask_loop_running = False

    def add_command(
        self, mode_name, to_hub_fmt="", from_hub_fmt="", command_type=CALLBACK
    ):
        super().add_command(mode_name, to_hub_fmt, from_hub_fmt, command_type)
        # Check the newly added commands against the advertised modes.
        modes = self.pup_device.info()["modes"]
        n = len(self.commands) - 1  # Zero indexed mode number
        assert len(self.commands) <= len(modes), "More commands than on remote side"
        assert (
            mode_name == modes[n][0].rstrip()
        ), f"Expected '{modes[n][0].rstrip()}' as mode {n}, but got '{mode_name}'"
        assert (
            self.commands[-1][SIZE] == modes[n][1]
        ), f"Different parameter size than on remote side. Check formats."

    def call(self, mode_name: str, *argv, wait_ms=0):
        """
        Call a remote function on the sensor side with the mode_name you defined on both sides.

        :param mode_name: The name of the mode you defined on the sensor side.
        :type mode_name: str
        :param argv: As many arguments as you need to pass to the remote function.
        :type argv: Any
        :param wait_ms: The time to wait before reading after sending the call payload.
            Only applicable if there is a payload outbound from the hub. So not for channels or
            functions without parameters.
            Defaults to 0ms. A good value is `struct.calcsize(from_hub_fmt) * 1.5` (ms)
        :type wait_ms: int
        """
        assert (
            not run_task()
        ), "Use 'call_multitask' instead of 'call', with multiple start blocks or multitask blocks"

        mode = self.modes[mode_name]
        size = self.commands[mode][SIZE]

        if FROM_HUB_FORMAT in self.commands[mode]:
            num_args = self.commands[mode][ARGS_FROM_HUB]
            if num_args >= 0:
                assert (
                    len(argv) == num_args
                ), "Expected {} argument(s) in call '{}'".format(num_args, mode_name)
            payl = self.encode(size, self.commands[mode][FROM_HUB_FORMAT], *argv)
            self.pup_device.write(
                mode, self._int8_to_uint8(tuple(payl + b"\x00" * (size - len(payl))))
            )
            wait(wait_ms)

        data = self.pup_device.read(mode)
        size = len(data)
        raw_data = struct.pack("%db" % size, *data)
        result = self.decode(self.commands[mode][TO_HUB_FORMAT], raw_data)
        # Convert tuple size 1 to single value
        return result[0] if len(result) == 1 else result

    async def call_multitask(self, command_name: str, *argv, wait_ms=0):
        """
        Calls a remote function.
        This is the async version for use with Pybricks Multitask.
        Make sure to run 'process_calls()' as coroutine.

        :param command_name: The name of the command
        :type command_name: string
        :param Optionally, you can pass the <n_from_hub> number of parameters.

        :return: It will return a single value, or a list, depending on the value of <n_to_hub>.

        """
        if not self._multitask_loop_running:
            raise AssertionError(
                "Start 'process_calls' as a seperate task (coroutine) before using 'call_multitask()'"
            )

        result_holder = {"done": False, "result": None, "error": None}
        self._queue.append((command_name, argv, wait_ms, result_holder))

        while not result_holder["done"]:
            await wait(1)  # cooperative multitasking

        if result_holder["error"]:
            raise result_holder["error"]
        return result_holder["result"]

    async def _execute_call(self, mode_name: str, *argv, wait_ms=0):
        mode = self.modes[mode_name]
        size = self.commands[mode][SIZE]

        if FROM_HUB_FORMAT in self.commands[mode]:
            num_args = self.commands[mode][ARGS_FROM_HUB]
            if num_args >= 0:
                assert (
                    len(argv) == num_args
                ), "Expected {} argument(s) in call '{}'".format(num_args, mode_name)
            payl = self.encode(size, self.commands[mode][FROM_HUB_FORMAT], *argv)
            await self.pup_device.write(
                mode, self._int8_to_uint8(tuple(payl + b"\x00" * (size - len(payl))))
            )
            await wait(wait_ms)

        data = await self.pup_device.read(mode)
        size = len(data)
        raw_data = struct.pack("%db" % size, *data)
        result = self.decode(self.commands[mode][TO_HUB_FORMAT], raw_data)
        # Convert tuple size 1 to single value
        return result[0] if len(result) == 1 else result

    async def process_calls(self):
        """
        Process multitask MicroPUP calls in a queue to avoid EAGAIN or IOERR.
        """
        self._multitask_loop_running = True
        running = False
        while True:
            if self._queue and not running:
                running = True
                command_name, argv, wait_ms, result_holder = self._queue.pop(0)

                try:
                    result = await self._execute_call(
                        command_name, *argv, wait_ms=wait_ms
                    )
                    result_holder["result"] = result
                except Exception as e:
                    result_holder["error"] = e
                    print(e)
                    raise
                finally:
                    result_holder["done"] = True
                    running = False
            await wait(1)


if __name__ == "__main__":
    if side == "Sensor":
        # -------------------------------------------------
        # Example sensor-side (lms-esp32) program using process_async
        # -------------------------------------------------

        # This example reads a generic analog sensor every 200ms,
        # updates a 'value' channel, and responds to a 'reset' RPC.

        counter = 1

        async def reset():
            # Remote commands also need to be async!!
            global counter
            counter = 1
            print("Reset")
            await asyncio.sleep(1)
            return 1  # acknowledgement

        async def main():
            global counter
            pr = PUPRemoteSensor()

            # RPC: reset counter on hub request
            pr.add_command("reset", to_hub_fmt="repr")
            pr.add_channel("value", to_hub_fmt="f")

            # Start heartbeat/callback processing
            asyncio.create_task(pr.process_async())

            # User loop: read analog input and update channel
            while True:
                val = 1 / counter  # replace with actual sensor read
                pr.update_channel("value", float(val))
                counter += 1
                # Yes: the main loop can be slow without hindering the heartbeat!
                await asyncio.sleep(0.5)

        try:
            asyncio.run(main())
        finally:
            asyncio.new_event_loop()

    elif side == "Hub":
        # -------------------------------------------------
        # Example hub-side program using process_async
        # -------------------------------------------------
        from pybricks.parameters import Port
        from pybricks.tools import multitask, run_task

        pr = PUPRemoteHub(Port.A)
        pr.add_command("reset", to_hub_fmt="repr")
        pr.add_channel("value", to_hub_fmt="f")

        async def main1():
            # User program. Put anything you like in here.
            while True:
                await wait(50)
                val = await pr.call_multitask("value")
                print(val)

        async def main2():
            # User program. Put anything you like in here.
            for i in range(10):
                await wait(1000)
                val = await pr.call_multitask("reset")
                print(val)

        async def main():
            # race=True ensures the program finishes when the first user thread is done.
            await multitask(main1(), main2(), pr.process_calls(), race=True)

        run_task(main())
