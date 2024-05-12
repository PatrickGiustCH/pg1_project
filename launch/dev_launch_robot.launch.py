from launch import LaunchDescription
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import os
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch.actions import TimerAction



from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    package_name='pg1_project' 

    joystick = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','joystick.launch.py'
                )]), launch_arguments={'use_sim_time': 'false'}.items()
    )

    slam = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','online_async_launch.py'
                )]), launch_arguments={'use_sim_time': 'false'}.items()
    )

    navigation = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','navigation_launch.py'
                )]), launch_arguments={'use_sim_time': 'false'}.items()
    )


    rviz_config_file = PathJoinSubstitution(
        [
            get_package_share_directory(package_name),
            "config",
            "rviz_navigation.rviz"
        ]
    )

    image_transport_node = Node(
        package='image_transport',
        executable='republish',
        name='image_republisher',
        arguments=['compressed', 'raw'],
        remappings=[
            ('in/compressed', '/camera/image_raw/compressed'),
            ('out', '/camera/image_raw/uncompressed')
        ]
    )

    rviz_node = Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            arguments=["-d", rviz_config_file],
        )

    delayed = TimerAction(period=2.0,
        actions=[rviz_node,slam])

    return LaunchDescription([
        joystick,
        navigation,
        image_transport_node,
        delayed
    ])