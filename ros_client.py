import roslibpy
import time

# ros_client = roslibpy.Ros(host="192.168.0.210", port=9090)
ros_client = roslibpy.Ros(host="localhost", port=9090)
ros_client.run()


def on_message_received(message):
    print("Received message:", message)


subscription = roslibpy.Topic(
    ros_client, "/robot_arm2", "trajectory_msgs/JointTrajectoryPoint"
)
subscription.subscribe(on_message_received)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    ros_client.terminate()
