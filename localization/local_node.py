import rclpy
import numpy as np
import math
import random

from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid, Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import PoseWithCovarianceStamped

class ParticleFilterLocalization(Node):

```
def __init__(self):
    super().__init__('localization_node')

    # -----------------------------
    # Parameters
    # -----------------------------
    self.num_particles = 200

    # particles: [x, y, theta, weight]
    self.particles = None

    # map storage
    self.map = None

    # odom memory
    self.last_odom = None

    # -----------------------------
    # ROS I/O
    # -----------------------------
    self.create_subscription(OccupancyGrid, '/map_lidar', self.map_cb, 10)
    self.create_subscription(LaserScan, '/scan', self.scan_cb, 10)
    self.create_subscription(Odometry, '/odom', self.odom_cb, 10)

    self.pose_pub = self.create_publisher(
        PoseWithCovarianceStamped,
        '/estimated_pose',
        10
    )

    self.timer = self.create_timer(0.2, self.update)

    self.get_logger().info("Particle Filter Localizer started")

# -----------------------------
# Callbacks
# -----------------------------
def map_cb(self, msg):
    self.map = msg

    if self.particles is None:
        self.init_particles()

def odom_cb(self, msg):
    self.current_odom = msg

def scan_cb(self, msg):
    self.current_scan = msg

# -----------------------------
# Initialize particles randomly
# -----------------------------
def init_particles(self):
    self.get_logger().info("Initializing particles...")

    self.particles = []

    for _ in range(self.num_particles):
        x = random.uniform(-2.0, 2.0)
        y = random.uniform(-2.0, 2.0)
        theta = random.uniform(-math.pi, math.pi)
        w = 1.0 / self.num_particles

        self.particles.append([x, y, theta, w])

# -----------------------------
# Motion model
# -----------------------------
def motion_update(self, dx, dy, dtheta):

    for p in self.particles:

        noise_x = random.gauss(0, 0.02)
        noise_y = random.gauss(0, 0.02)
        noise_t = random.gauss(0, 0.01)

        p[0] += dx + noise_x
        p[1] += dy + noise_y
        p[2] += dtheta + noise_t

# -----------------------------
# Sensor model (VERY simplified scan match)
# -----------------------------
def compute_weight(self, particle):
    # Normally you'd raycast into map here
    # We approximate using map bounds only

    x, y, theta, _ = particle

    if self.map is None:
        return 1.0

    width = self.map.info.width
    height = self.map.info.height

    # crude scoring: stay inside map = better
    if 0 < x < width and 0 < y < height:
        return 1.0
    else:
        return 0.01

# -----------------------------
# Resampling
# -----------------------------
def resample(self):

    weights = np.array([p[3] for p in self.particles])
    weights += 1e-9
    weights /= np.sum(weights)

    indices = np.random.choice(
        len(self.particles),
        len(self.particles),
        p=weights
    )

    new_particles = []
    for i in indices:
        x, y, t, _ = self.particles[i]
        new_particles.append([x, y, t, 1.0 / self.num_particles])

    self.particles = new_particles

# -----------------------------
# Main loop
# -----------------------------
def update(self):

    if self.map is None or not hasattr(self, 'current_scan'):
        return

    # -----------------------------
    # motion update from odom
    # -----------------------------
    if self.last_odom is not None:

        dx = self.current_odom.pose.pose.position.x - self.last_odom.pose.pose.position.x
        dy = self.current_odom.pose.pose.position.y - self.last_odom.pose.pose.position.y
        dtheta = 0.0

        self.motion_update(dx, dy, dtheta)

    self.last_odom = self.current_odom

    # -----------------------------
    # weight particles
    # -----------------------------
    for p in self.particles:
        p[3] = self.compute_weight(p)

    # -----------------------------
    # resample
    # -----------------------------
    self.resample()

    # -----------------------------
    # estimate pose
    # -----------------------------
    x = np.mean([p[0] for p in self.particles])
    y = np.mean([p[1] for p in self.particles])
    t = np.mean([p[2] for p in self.particles])

    # -----------------------------
    # publish pose
    # -----------------------------
    msg = PoseWithCovarianceStamped()
    msg.header.stamp = self.get_clock().now().to_msg()
    msg.header.frame_id = "map"

    msg.pose.pose.position.x = float(x)
    msg.pose.pose.position.y = float(y)

    msg.pose.pose.orientation.z = math.sin(t / 2.0)
    msg.pose.pose.orientation.w = math.cos(t / 2.0)

    self.pose_pub.publish(msg)
```

def main(args=None):
rclpy.init(args=args)
node = ParticleFilterLocalization()
rclpy.spin(node)
node.destroy_node()
rclpy.shutdown()

if **name** == '**main**':
main()
