import asyncio
import websockets
import json
import orjson

# from pros_car_py.car_models import DeviceDataTypeEnum, CarBControl
import pydantic
from typing import List
from enum import Enum, auto


class StringEnum(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __eq__(self, other):
        if isinstance(other, StringEnum):
            return self.value == other.value
        elif isinstance(other, str):
            return self.value == other
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.value

    def __hash__(self):
        return hash(self.value)


class DeviceDataTypeEnum(StringEnum):
    car_B_state = auto()
    car_B_control = auto()
    robot_arm = auto()


class DeviceData(pydantic.BaseModel):
    type: DeviceDataTypeEnum
    data: dict


class CarBControl(pydantic.BaseModel):
    target_vel: List[float] = []


async def advertise_topic(websocket):
    advertise_message = {
        "op": "advertise",
        "topic": str(DeviceDataTypeEnum.car_B_control),
        "type": "std_msgs/String",
    }
    await websocket.send(json.dumps(advertise_message))
    print(f"Advertised topic: {advertise_message}")


async def publish_to_writer(left_wheel_value, right_wheel_value):
    uri = "ws://192.168.0.210:9090"

    async with websockets.connect(uri) as websocket:
        await advertise_topic(websocket)

        control_signal = {
            "type": str(DeviceDataTypeEnum.car_B_control),
            "data": dict(CarBControl(target_vel=[left_wheel_value, right_wheel_value])),
        }
        control_msg = {
            "op": "publish",
            "topic": str(DeviceDataTypeEnum.car_B_control),
            "msg": {"data": orjson.dumps(control_signal).decode()},
        }
        await websocket.send(json.dumps(control_msg))
        print(f"Message sent: {control_msg}")


def value_ratio(value):
    old_min, old_max = -10, 10
    new_min, new_max = -30, 30
    mapped_value = new_min + (value - old_min) * (new_max - new_min) / (
        old_max - old_min
    )
    print(mapped_value)
    return mapped_value


# 輪速設定限制在10~-10之間
def set_two_wheel(left_wheel_value, right_wheel_value):
    asyncio.get_event_loop().run_until_complete(
        publish_to_writer(value_ratio(left_wheel_value), value_ratio(right_wheel_value))
    )


def car_forward():
    set_two_wheel(5, 5)


def car_back():
    set_two_wheel(-5, -5)


# 左自轉
def car_counterclockwise_rotate():
    set_two_wheel(-5, 5)


# 右自轉
def car_clockwise_rotate():
    set_two_wheel(5, -5)


# 左斜轉
def car_left_lean():
    set_two_wheel(2, 5)


# 右斜轉
def car_right_lean():
    set_two_wheel(5, 2)


def car_stop():
    set_two_wheel(0, 0)


def main(args=None):
    car_stop()


if __name__ == "__main__":
    main()
