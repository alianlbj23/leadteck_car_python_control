import roslibpy
import math
import time

# 创建ROS客户端
ros_client = roslibpy.Ros(host="192.168.0.210", port=9090)
ros_client.run()

# 定义话题
car_control_topic = roslibpy.Topic(
    ros_client, "/robot_arm", "trajectory_msgs/JointTrajectoryPoint"
)


def publish_to_writer(
    positions, velocities=None, accelerations=None, effort=None, time_from_start=None
):
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
    print("Publishing:", control_signal)
    car_control_topic.publish(roslibpy.Message(control_signal))


def degree_to_radian(value_list):
    return [math.radians(value) for value in value_list]


def reset_robot_arm():
    reset_radian = degree_to_radian([90, 100, 20, 80, 30, 0])
    publish_to_writer(positions=reset_radian)


def main():
    reset_robot_arm()


if __name__ == "__main__":
    main()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        ros_client.terminate()
