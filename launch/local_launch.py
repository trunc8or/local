from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

```
localization_node = Node(
    package='local',
    executable='localization_node',
    name='localization_node',
    output='screen'
)

return LaunchDescription([
    localization_node
])
```
