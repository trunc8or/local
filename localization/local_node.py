import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseWithCovarianceStamped

class LocalizationNode(Node):

```
def __init__(self):

    super().__init__('localization_node')

    # Subscribe to AMCL output
    self.amcl_sub = self.create_subscription(
        PoseWithCovarianceStamped,
        '/amcl_pose',
        self.amcl_callback,
        10
    )

    # Optional: re-publish for your system
    self.pose_pub = self.create_publisher(
        PoseWithCovarianceStamped,
        '/estimated_pose',
        10
    )

    self.get_logger().info("AMCL interface node started")

def amcl_callback(self, msg):

    # Directly forward AMCL pose
    self.pose_pub.publish(msg)

    self.get_logger().info(
        f"Pose: x={msg.pose.pose.position.x:.2f}, "
        f"y={msg.pose.pose.position.y:.2f}"
    )
```

def main(args=None):
rclpy.init(args=args)
node = LocalizationNode()
rclpy.spin(node)
node.destroy_node()
rclpy.shutdown()

if **name** == '**main**':
main()
