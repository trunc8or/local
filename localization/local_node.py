import rclpy
import numpy as np
from rclpy.node import Node

from nav_msgs.msg import OccupancyGrid, Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import PoseWithCovarianceStamped

class LocalizationNode(Node):

```
def __init__(self):

    super().__init__('localization_node')

    # State
    self.map = None
    self.odom = None
    self.scan = None

    # Publisher (THIS is the output of localization)
    self.pose_pub = self.create_publisher(
        PoseWithCovarianceStamped,
        '/estimated_pose',
        10
    )

    # Subscriptions
    self.create_subscription(OccupancyGrid, '/map_lidar', self.map_cb, 10)
    self.create_subscription(LaserScan, '/scan', self.scan_cb, 10)
    self.create_subscription(Odometry, '/odom', self.odom_cb, 10)

    self.get_logger().info("Localization node started")

    # Timer runs localization loop
    self.timer = self.create_timer(0.2, self.update)

def map_cb(self, msg):
    self.map = msg

def scan_cb(self, msg):
    self.scan = msg

def odom_cb(self, msg):
    self.odom = msg

def update(self):
    if self.map is None or self.scan is None or self.odom is None:
        return

    # ---- STEP 1: use odom as initial guess ----
    x = self.odom.pose.pose.position.x
    y = self.odom.pose.pose.position.y

    # Simple orientation extraction (yaw)
    q = self.odom.pose.pose.orientation
    yaw = self.quaternion_to_yaw(q)

    # ---- STEP 2: pretend we "refine" pose ----
    # (this is where real scan matching / particle filter goes)
    refined_x = x
    refined_y = y
    refined_yaw = yaw

    # ---- STEP 3: publish pose ----
    msg = PoseWithCovarianceStamped()
    msg.header.stamp = self.get_clock().now().to_msg()
    msg.header.frame_id = "map"

    msg.pose.pose.position.x = refined_x
    msg.pose.pose.position.y = refined_y

    msg.pose.pose.orientation = q

    self.pose_pub.publish(msg)

def quaternion_to_yaw(self, q):
    import math
    siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    return math.atan2(siny_cosp, cosy_cosp)
```

def main(args=None):
rclpy.init(args=args)
node = LocalizationNode()
rclpy.spin(node)
node.destroy_node()
rclpy.shutdown()

if **name** == '**main**':
main()
