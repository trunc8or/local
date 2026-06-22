# Local

ROS 2 package for robot localization.

## Goal

Estimate the robot's pose on a known occupancy grid map using:

* LiDAR scans (`/scan`)
* Odometry (`/odom`)
* Occupancy grid map (`/map`)

The robot should be able to determine its position on a known map even when starting from an unknown location.

## Package Structure

```text
local/
├── launch/
├── config/
├── resource/
├── localization/
├── package.xml
├── setup.py
└── setup.cfg
```

## Build

```bash
cd ~/ws
colcon build --symlink-install
source install/setup.bash
```

## Run

```bash
ros2 run local localization_node
```

or

```bash
ros2 launch local localization.launch.py
```

## Topics

### Subscribed

* `/map`
* `/scan`
* `/odom`

### Published

* `/estimated_pose`

## Author

Rory O'Brien
