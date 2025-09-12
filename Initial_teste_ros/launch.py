from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='diferencial',
            namespace='ros_ws',
            executable='no',
            name='no'
        )
    ])
