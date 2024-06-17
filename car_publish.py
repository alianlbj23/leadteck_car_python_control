import asyncio
import websockets
import json
import orjson
from pros_car_py.car_models import DeviceDataTypeEnum, CarBControl

async def advertise_topic(websocket):
    advertise_message = {
        "op": "advertise",
        "topic": str(DeviceDataTypeEnum.car_B_control),
        "type": "std_msgs/String"
    }
    await websocket.send(json.dumps(advertise_message))
    print(f"Advertised topic: {advertise_message}")

async def publish_to_writer(left_wheel_value, right_wheel_value):
    uri = "ws://localhost:9090"  # 连接到本地的rosbridge

    async with websockets.connect(uri) as websocket:
        # 先广告话题
        await advertise_topic(websocket)

        # 创建控制信号
        control_signal = {
            "type": str(DeviceDataTypeEnum.car_B_control),
            "data": dict(CarBControl(target_vel=[left_wheel_value, right_wheel_value])),
        }
        # 将控制信号转换为JSON字符串
        control_msg = {
            "op": "publish",
            "topic": str(DeviceDataTypeEnum.car_B_control),  # 使用你要发布的topic
            "msg": {
                "data": orjson.dumps(control_signal).decode()
            }
        }
        # 发送消息
        await websocket.send(json.dumps(control_msg))
        print(f"Message sent: {control_msg}")

def value_ratio(value):
    old_min, old_max = -10, 10
    new_min, new_max = -30, 30
    mapped_value = new_min + (value - old_min) * (new_max - new_min) / (old_max - old_min)
    return mapped_value

def set_two_wheel(left_wheel_value, right_wheel_value):
    asyncio.get_event_loop().run_until_complete(
        publish_to_writer(value_ratio(left_wheel_value), value_ratio(right_wheel_value))
    )

def main(args=None):
    set_two_wheel(5, -5)

if __name__ == "__main__":
    main()
