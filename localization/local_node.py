import rclpy

from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan

class LocalizationNode(Node):

```
def __init__(self):

    super().__init__('localization_node')

    self.map_received = False
    self.scan_received = False
    self.odom_received = False

    self.map_sub = self.create_subscription(
        OccupancyGrid,
        '/map_lidar',
        self.map_callback,
        10
    )

    self.scan_sub = self.create_subscription(
        LaserScan,
        '/scan',
        self.scan_callback,
        10
    )

    self.odom_sub = self.create_subscription(
        Odometry,
        '/odom',
        self.odom_callback,
        10
    )

    self.get_logger().info('Localization node started')

def map_callback(self, msg):

    if not self.map_received:

        self.map_received = True

        self.get_logger().info(
            f'Received map: {msg.info.width} x {msg.info.height}'
        )

def scan_callback(self, msg):

    if not self.scan_received:

        self.scan_received = True

        self.get_logger().info(
            f'Received laser scan with {len(msg.ranges)} ranges'
        )

def odom_callback(self, msg):

    if not self.odom_received:

        self.odom_received = True

        self.get_logger().info(
            'Received odometry'
        )
```

def main(args=None):

```
rclpy.init(args=args)

node = LocalizationNode()

rclpy.spin(node)

node.destroy_node()

rclpy.shutdown()
```

if **name** == '**main**':
main()
