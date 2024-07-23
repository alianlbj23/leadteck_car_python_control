import roslibpy
import math
import time

# 创建ROS客户端
ros_client = roslibpy.Ros(host="192.168.0.210", port=9090)
ros_client.run()

# 定义发布和订阅的话题
car_control_topic = roslibpy.Topic(
    ros_client, "/robot_arm", "trajectory_msgs/JointTrajectoryPoint"
)

previous_state_topic = roslibpy.Topic(
    ros_client, "/robot_arm", "trajectory_msgs/JointTrajectoryPoint"
)

# 初始默认关节状态（假设有6个关节）
default_positions = [
    math.radians(90),
    math.radians(100),
    math.radians(20),
    math.radians(80),
    math.radians(30),
    0,
]
last_positions = default_positions.copy()


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
    time.sleep(0.5)


def degree_to_radian(value_list):
    new_list = []
    for value in value_list:
        if value == -1:
            new_list.append(-1)
        else:
            new_list.append(math.radians(value))
    return new_list
    # return [math.radians(value) for value in value_list if value is not None]


def radian_to_degree(value_list):
    return [math.degrees(value) for value in value_list if value is not None]


def reset_robot_arm():
    reset_radian = degree_to_radian([90, 90, 175, 90, 90, 0])
    # reset_radian = degree_to_radian([150, 20, 100, 70, 90, 0])
    publish_to_writer(positions=reset_radian)


def axis1_arm():
    new_angle = degree_to_radian([-1, -1, -1, 10, -1, -1])
    publish_to_writer(positions=new_angle)


def state_callback(message):
    global last_positions
    last_positions = message["positions"]
    print("Received previous data:", last_positions)


# 往前座像夾取的動作
def boxing1():
    degree1 = degree_to_radian([90, 150, 125, 170, 50, 0])
    degree2 = degree_to_radian([90, 50, 90, 120, 90, 0])
    combine = [degree1, degree2]
    for degree in combine:
        publish_to_writer(degree)
        time.sleep(1.5)


# 左右搖擺
def shake_left_and_right():
    reset1 = degree_to_radian([90, 100, 130, 150, 90, 0])
    degree1 = degree_to_radian([50, 100, 130, 150, 90, 0])
    degree2 = degree_to_radian([120, 100, 130, 150, 90, 0])
    publish_to_writer(reset1)
    time.sleep(1)
    combine = [degree1, degree2]
    for i in range(5):
        for degree in combine:
            publish_to_writer(degree)
            time.sleep(1)


# 上下晃動
def shake_up():
    reset1 = degree_to_radian([90, 30, 100, 30, 90, 0])
    degree1 = degree_to_radian([90, 80, 100, 30, 90, 0])
    combine = [reset1, degree1]
    for degree in combine:
        publish_to_writer(degree)
        time.sleep(1)


# 袈裟斬り！
def kesagiri():
    reset1 = degree_to_radian([40, 60, 70, 70, 90, 0])
    degree1 = degree_to_radian([150, 20, 100, 70, 90, 0])
    combine = [reset1, degree1]
    for degree in combine:
        publish_to_writer(degree)
        time.sleep(1)


def main():
    # # 订阅获取上一次发布的关节状态
    # previous_state_topic.subscribe(state_callback)
    # print("Subscribed to /robot_arm topic to receive previous data.")

    # # 等待一定时间以确保接收到消息
    # time.sleep(5)

    # # 打印上一次接收到的信号
    # print("Last positions:", radian_to_degree(last_positions))

    # # 取消订阅
    # previous_state_topic.unsubscribe()
    # boxing1()
    reset_robot_arm()
    # kesagiri()
    # shake1()
    # axis1_arm()


if __name__ == "__main__":
    main()
