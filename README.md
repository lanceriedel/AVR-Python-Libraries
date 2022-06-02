# VRC-Python-Libraries

## Install

To install the base package, run:

```bash
pip install bell-vrc-libraries
```

Additionally, the `mqtt` and `serial` extras are available if you want to use
the MQTT or PCC functionality.

```bash
pip install bell-vrc-libraries[mqtt,serial]
```

## Usage

### MQTT

```python
from bell.vrc import mqtt
```

These are MQTT utilities that are used to have a consistent messaging protocol
throughout all the VRC software modules.

The first part of this are the payloads for the MQTT messages themselves. As VRC
exclusively uses JSON, these are all
[`TypedDict`](https://docs.python.org/3/library/typing.html#typing.TypedDict)s
that have all of the required fields for a message.

Example:

```python
from bell.vrc.mqtt.messages import VrcPcmSetBaseColorMessage

message = VrcPcmSetBaseColorMessage((128, 232, 142, 0))
```

The second part of the MQTT libraries, is the `MQTTModule` class.
This is a boilerplate module for VRC that makes it very easy to send
and recieve MQTT messages and do something with them.

Example:

```python
from bell.vrc.mqtt.client import MQTTModule
from bell.vrc.mqtt.messages import VrcFcmVelocityMessage, VrcPcmSetServoOpenCloseMessage


class Sandbox(MQTTModule):
    def __init__(self) -> None:
        self.topic_map = {"vrc/fcm/velocity": self.show_velocity}

    def show_velocity(self, payload: VrcFcmVelocityMessage) -> None:
        vx = payload["vX"]
        vy = payload["vY"]
        vz = payload["vZ"]
        v_ms = (vx, vy, vz)
        print(f"Velocity information: {v_ms} m/s")

    def open_servo(self) -> None:
        message = VrcPcmSetServoOpenCloseMessage(servo=0, action="open")
        self.send_message("vrc/pcm/set_servo_open_close", message)


if __name__ == "__main__":
    box = Sandbox()
    box.run()
```

The `topic_map` dictionary is a class attribute that maps topics to subscribe to
and a function that will handle an incoming payload. The `payload` argument
should match the appropriate `Message` class for that topic.

Additionally, the `message_cache` attribute is a dictionary that holds
a copy of the last payload sent by that module on a given topic. The keys are the
topic strings, and the values are the topic payloads.

### Utilities

```python
from bell.vrc import utils
```

These are general purpose utilities.

There are 3 different function decorators available, which are helpful for MQTT
message callbacks. First is the `try_except` decorator, which wraps the
function in a `try: except:` statement and will log any exceptions to the console:

```python
    from bell.vrc.utils.decorators import try_except

    @try_except
    def assemble_hil_gps_message(self) -> None:
        ...
```

Additionally, there is the `reraise` argument, which can be set to `True` to raise
any exceptions that are encountered. This is helpful if you still want exceptions
to propagate up, but log them.

There is an async version of this decorator as well with an `async_` prefix.

```python
    @async_try_except()
    async def connected_status_telemetry(self) -> None:
        ...
```

The last decorator is `run_forever` which will run the wrapped function forever,
with a given `period` or `frequency`.

```python
    @run_forever(frequency=5)
    def read_data(self) -> None:
        ...
```

Lastly, there is a `rate_limit` function which take a callable and a
period or frequency, and only run the callable at that given rate.

```python
for _ in range(10):
    # add() will only run twice
    rate_limit(add, period=5)
    time.sleep(1)
```

## Development

Install [`poetry`](https://python-poetry.org/) and run `poetry install --extras mqtt --extras serial`.

Build the auto-generated code with `poetry run python build.py`.
