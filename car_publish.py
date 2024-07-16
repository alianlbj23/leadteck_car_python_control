"""
created_at_utc  : 2024-07-01T02:39:25Z
created_at_w3c  : 2024-07-01T10:39:25+08:00
PROS-Blocks     : 0.0.2
"""

import roslibpy
import orjson
import time

ros_client = roslibpy.Ros(host="localhost", port=9090)
ros_client.run()

car_control_topic = roslibpy.Topic(ros_client, "car_B_control", "std_msgs/String")


def publish_to_writer(left_wheel_value, right_wheel_value):
    control_signal = {
        "type": "car_B_control",
        "data": {"target_vel": [left_wheel_value, right_wheel_value]},
    }
    control_msg = {"data": orjson.dumps(control_signal).decode()}
    car_control_topic.publish(control_msg)


def value_ratio(value):
    if value > 10:
        value = 10
    elif value < -10:
        value = -10
    old_min, old_max = -10, 10
    new_min, new_max = -30, 30
    mapped_value = new_min + (value - old_min) * (new_max - new_min) / (
        old_max - old_min
    )
    return mapped_value


def set_two_wheel(left_wheel_value, right_wheel_value):
    publish_to_writer(value_ratio(left_wheel_value), value_ratio(right_wheel_value))
    time.sleep(0.1)


set_two_wheel(5, 5)
