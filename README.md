# Robot Localization (AMCL-based)

This package provides a simple interface to ROS 2 AMCL localization.

It does NOT implement localization itself — instead it uses AMCL from Nav2.

---

# Goal

Get a reliable estimate of robot pose:

```text id="r1"
/estimated_pose
```

in the map frame using a known occupancy grid map.

---

# System Overview

The system consists of three parts:

---

## 1. SLAM (Map Provider)

Run:

```bash id="r2"
ros2 launch slam slam.launch.py
```

Publishes:

* `/map_lidar` (OccupancyGrid)
* `map → odom` transform

---

## 2. AMCL (Localization Engine)

AMCL is provided by Nav2 and performs:

* particle filter localization
* scan matching against occupancy grid
* pose estimation in map frame

It publishes:

* `/amcl_pose`
* TF: `map → odom`

---

## 3. This Package (Interface Layer)

This package:

* subscribes to `/amcl_pose`
* republishes `/estimated_pose`
* logs robot position

It does NOT compute localization itself.

---

# Data Flow

```text id="r3"
SLAM → /map_lidar
          ↓
        AMCL
          ↓
     /amcl_pose
          ↓
  local package node
          ↓
   /estimated_pose
```

---

# Topics

## Subscribed

| Topic      | Type                      | Source |
| ---------- | ------------------------- | ------ |
| /amcl_pose | PoseWithCovarianceStamped | AMCL   |

---

## Published

| Topic           | Type                      | Purpose             |
| --------------- | ------------------------- | ------------------- |
| /estimated_pose | PoseWithCovarianceStamped | cleaned pose output |

---

# How to Run

## 1. Start SLAM (map provider)

```bash id="r4"
ros2 launch slam slam.launch.py
```

---

## 2. Start AMCL (Nav2 localization)

```bash id="r5"
ros2 launch nav2_bringup localization_launch.py map:=<your_map.yaml>
```

---

## 3. Start this interface node

```bash id="r6"
ros2 launch local local_launch.py
```

---

# Visualization (RViz2)

Add displays:

* Map → `/map_lidar`
* LaserScan → `/scan`
* Pose → `/amcl_pose` or `/estimated_pose`
* TF → enabled

---

# Why AMCL is used

AMCL provides:

* robust localization
* proven particle filter implementation
* automatic recovery from lost localization
* industry-standard solution in ROS 2 Nav2

---

# What this package adds

This package is a lightweight wrapper that:

* simplifies access to pose data
* standardizes output topic `/estimated_pose`
* allows future integration with other modules

---

# Summary

* SLAM builds the map
* AMCL finds the robot in the map
* this package forwards the pose for other systems
