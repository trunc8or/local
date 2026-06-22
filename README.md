# Localisation (ROS 2)

This package implements a **particle-filter based robot localisation system** for a mobile robot using a pre-built occupancy grid map.

---

# Goal

Estimate the robot’s pose:

```text
(x, y, θ)
```

in the **map frame**, even when the robot is placed at a random position.

---

# System Overview

The system is split into two parts:

## 1. SLAM (mapping system)

Run separately:

```bash
ros2 launch slam slam.launch.py
```

It publishes:

* `/map_lidar` → OccupancyGrid map
* `map → odom` transform

This provides a **known static map** for localisation.

---

## 2. Localisation (this package)

This package subscribes to:

* `/map_lidar` (OccupancyGrid)
* `/scan` (LaserScan)
* `/odom` (Odometry)

and estimates the robot pose using a **particle filter**.

It publishes:

* `/estimated_pose` (PoseWithCovarianceStamped)

---

# Localisation Algorithm (what the code does)

This implementation uses a **particle filter**, which works as follows:

---

## Step 1: Particles

We maintain many hypotheses of the robot pose:

```text
particle = (x, y, θ, weight)
```

Each particle represents a possible robot position.

---

## Step 2: Motion Model (odometry update)

Robot movement from `/odom` is used to move all particles:

```text
new_pose = old_pose + odom_delta + noise
```

This predicts where the robot might have moved.

---

## Step 3: Sensor Model (laser + map comparison)

Each particle is scored based on how well it matches the environment.

Intuition:

* If a particle explains the laser scan well → high weight
* If it does not match the map → low weight

---

## Step 4: Resampling

Particles with higher weights are kept.

Bad particles are discarded.

This concentrates guesses around the correct pose.

---

## Step 5: Pose Estimate

Final robot pose is computed as:

```text
average of all particle poses
```

and published as:

```
/estimated_pose
```

---

# ROS Graph

```text
          /map_lidar
SLAM  ------------------+
                        |
          /scan         v
LiDAR  ------------>  Localization Node  ----> /estimated_pose
                        ^
          /odom         |
Robot ------------------+
```

---

# How to run

## 1. Start SLAM (map provider)

```bash
ros2 launch slam slam.launch.py
```

---

## 2. Start localisation

```bash
ros2 launch local local_launch.py
```

---

## 3. Visualise in RViz

Add:

* Map → `/map_lidar`
* LaserScan → `/scan`
* Pose → `/estimated_pose`

---

# File Structure

```text
local/
├── launch/
│   └── local_launch.py
├── config/
│   └── local.yaml
├── localization/
│   ├── __init__.py
│   └── localization_node.py
├── resource/
├── package.xml
├── setup.py
└── setup.cfg
```

---

# Topics

## Subscribed

| Topic      | Type                   | Purpose         |
| ---------- | ---------------------- | --------------- |
| /map_lidar | nav_msgs/OccupancyGrid | environment map |
| /scan      | sensor_msgs/LaserScan  | LiDAR data      |
| /odom      | nav_msgs/Odometry      | motion estimate |

---

## Published

| Topic           | Type                      | Purpose                 |
| --------------- | ------------------------- | ----------------------- |
| /estimated_pose | PoseWithCovarianceStamped | robot pose in map frame |

---

# Important Notes

* SLAM is **not part of this package**
* This package assumes the map is already known
* Localization improves odometry using laser + map alignment
* Particle filter is a probabilistic estimation method

---

# Limitations (current version)

* Sensor model is simplified (not full ray-casting yet)
* Accuracy depends on map quality
* Performance depends on number of particles

---

# Next improvements (if needed)

* Replace simple scoring with ray-casting
* Add proper likelihood field model
* Improve initialization (global localization)
* Tune particle count for performance

---

# Summary

This system answers:

> “Where am I on a known map?”

by combining:

* motion (odometry)
* perception (LiDAR)
* map knowledge (occupancy grid)

using a **particle filter probabilistic estimator**.
