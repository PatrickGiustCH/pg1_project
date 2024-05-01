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

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )


    robot_controllers = PathJoinSubstitution(
        [
            FindPackageShare(package_name),
            "config",
            "my_controllers.yaml",
        ]
    )




    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[{"robot_description": Command(['ros2 param get --hide-type /robot_state_publisher robot_description'])}, robot_controllers],
        output="both",
    )


    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "-c", "/controller_manager"],
    )

    robot_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diffbot_base_controller", "-c", "/controller_manager"],
    )

    delayed = TimerAction(period=1.0,
            actions=[control_node, joint_state_broadcaster_spawner,robot_controller_spawner])
    
    return LaunchDescription([
        rsp,
        delayed

    ])