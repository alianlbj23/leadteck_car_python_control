import roslibpy
import time

# 初始化 ROS Bridge 客戶端
client = roslibpy.Ros(host="localhost", port=9090)
client.run()

# 定義 JointTrajectoryPoint 訊息的發布主題
publisher = roslibpy.Topic(
    client, "/joint_trajectory_point", "trajectory_msgs/JointTrajectoryPoint"
)

# 創建 JointTrajectoryPoint 訊息
joint_trajectory_point = roslibpy.Message(
    {
        "positions": [1.0, 0.5, 0.0],
        "velocities": [0.1, 0.1, 0.1],
        "accelerations": [0.01, 0.01, 0.01],
        "effort": [0.0, 0.0, 0.0],
        "time_from_start": {"secs": 1, "nsecs": 0},
    }
)


# 發布訊息
def publish_message():
    publisher.publish(joint_trajectory_point)
    print("Message published.")


# 持續發布訊息
try:
    while True:
        publish_message()
        time.sleep(1)
except KeyboardInterrupt:
    pass

# 釋放資源
publisher.unadvertise()
client.terminate()
