"""
created_at_utc  : 2024-07-01T02:39:25Z
created_at_w3c  : 2024-07-01T10:39:25+08:00
PROS-Blocks     : 0.0.2
"""

import roslibpy
import orjson
import time

ros_client = roslibpy.Ros(host="192.168.0.210", port=9090)
ros_client.run()

car_control_topic = roslibpy.Topic(ros_client, "robot_arm", "trajectory_msgs/msg/JointTrajectoryPoint")


def publish_to_writer(positions, velocities=None, accelerations=None, effort=None, time_from_start=None):
    if velocities is None:
        velocities = [0.0] * len(positions)
    if accelerations is None:
        accelerations = []
    if effort is None:
        effort = []
    if time_from_start is None:
        time_from_start = {"sec": 0, "nanosec": 0}

    control_signal = {
        "positions": positions,
        "velocities": velocities,
        "accelerations": accelerations,
        "effort": effort,
        "time_from_start": time_from_start,
    }
    control_msg = {"data": orjson.dumps(control_signal).decode()}
    car_control_topic.publish(control_msg)


def degree_to_radian(value):
    return [math.radians(value) for value in value_list]

# {90, 100, 20, 80, 30, 0}
def reset_robot_arm():
    reset_radian = degree_to_radian([90, 100, 20, 80, 30, 0])
    publish_to_writer(positions=reset_radian)

reset_robot_arm()
