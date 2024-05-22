from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.conditions import UnlessCondition

import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():


    params_file = LaunchConfiguration('params_file')
    params_file_dec = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(get_package_share_directory('pg1_project'),'config','circle_tracker_params.yaml'),
        description='Full path to params file for all ball_tracker nodes.')

   



    detect_node = Node(
            package='ball_tracker',
            executable='detect_ball',
            parameters=[params_file],
            remappings=[('/image_in','/camera/image_raw')],
         )







    return LaunchDescription([
        params_file_dec,
        detect_node
    ])