import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, AppendEnvironmentVariable, DeclareLaunchArgument

from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterValue
from ament_index_python.packages import get_package_share_path


def generate_launch_description():

    cuchak_share = get_package_share_path('cuchak_description')

    urdf_path = os.path.join(
        cuchak_share, 'urdf', 'cuchak.urdf.xacro'
    )

    rviz_config_path = os.path.join(
        get_package_share_path('cuchak_description'),
        'rviz', 'config.rviz'
    )

    gz_sim_path = os.path.join(
        get_package_share_path('ros_gz_sim'),
        'launch', 'gz_sim.launch.py'
    )

    # Para que Gazebo encuentre model://cuchak_description/meshes/...
    set_resource_path = AppendEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH',
        os.path.dirname(str(cuchak_share))
    )

    gz_bridge_config_path = os.path.join(
        get_package_share_path('cuchak_gz_bringup'),
        'config', 'gz_bridge.yaml'
    )

    gz_worlds_folder_path = os.path.join(
        get_package_share_path('cuchak_gz_bringup'),
        'worlds'
    )

    world = LaunchConfiguration('world')

    gz_worlds_path = PathJoinSubstitution([
        gz_worlds_folder_path,
        world
    ])

    robot_description = ParameterValue(
        Command(['xacro ', urdf_path]),
        value_type=str
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{'robot_description': robot_description}]
    )

    gz_sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_sim_path),
        launch_arguments={
            'gz_args': [gz_worlds_path, ' -r -v 4']
        }.items()
    )

    gz_create_node = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-topic", "/robot_description",
            "-z", "0.0"
        ],
        output="screen"
    )

    gz_bridge_node = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        parameters=[{'config_file': gz_bridge_config_path}],
        output="screen"
    )

    rviz2_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d', rviz_config_path],
        parameters=[{'use_sim_time': True}]
    )

    return LaunchDescription([

        DeclareLaunchArgument(
            'world',
            default_value='empty.sdf',
            choices=['empty.sdf', 'moon.sdf'],
            description='Mundo de Gazebo que se va a cargar'
        ),

        set_resource_path,
        robot_state_publisher_node,
        gz_sim_launch,
        gz_create_node,
        gz_bridge_node,
        rviz2_node
    ])