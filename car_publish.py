import asyncio
import websockets
import json
import orjson

DEVICE_DATA_TYPE_ENUM = {"CAR_B_CONTROL": "car_B_control"}


def create_car_b_control(target_vel):
    return {"target_vel": target_vel}


async def advertise_topic(websocket):
    advertise_message = {
        "op": "advertise",
        "topic": DEVICE_DATA_TYPE_ENUM["CAR_B_CONTROL"],
        "type": "std_msgs/String",
    }
    await websocket.send(json.dumps(advertise_message))
    print(f"Advertised topic: {advertise_message}")


async def publish_to_writer(left_wheel_value, right_wheel_value):
    uri = "ws://192.168.0.210:9090"

    async with websockets.connect(uri) as websocket:
        await advertise_topic(websocket)

        control_signal = {
            "type": DEVICE_DATA_TYPE_ENUM["CAR_B_CONTROL"],
            "data": create_car_b_control([left_wheel_value, right_wheel_value]),
        }
        control_msg = {
            "op": "publish",
            "topic": DEVICE_DATA_TYPE_ENUM["CAR_B_CONTROL"],
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


def set_two_wheel(left_wheel_value, right_wheel_value):
    asyncio.get_event_loop().run_until_complete(
        publish_to_writer(value_ratio(left_wheel_value), value_ratio(right_wheel_value))
    )


def car_customize_wheel_value(left_wheel_value=0, right_wheel_value=0):
    set_two_wheel(left_wheel_value, right_wheel_value)


def car_forward():
    set_two_wheel(5, 5)


def car_back():
    set_two_wheel(-5, -5)


def car_counterclockwise_rotate():
    set_two_wheel(-5, 5)


def car_clockwise_rotate():
    set_two_wheel(5, -5)


def car_left_lean():
    set_two_wheel(2, 5)


def car_right_lean():
    set_two_wheel(5, 2)


def car_stop():
    set_two_wheel(0, 0)


def main(args=None):
    car_customize_wheel_value(0, 0)


if __name__ == "__main__":
    main()
