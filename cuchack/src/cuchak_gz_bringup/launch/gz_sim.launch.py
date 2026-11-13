import os

from launch import LaunchDescription  # type: ignore
from launch.actions import IncludeLaunchDescription, AppendEnvironmentVariable  # type: ignore
from launch.launch_description_sources import PythonLaunchDescriptionSource  # type: ignore
from launch.substitutions import Command  # type: ignore
from launch_ros.actions import Node  # type: ignore
from launch_ros.descriptions import ParameterValue  # type: ignore
from ament_index_python.packages import get_package_share_path  # type: ignore


def generate_launch_description():

    cuchak_share = get_package_share_path('cuchak_description')

    urdf_path = os.path.join(cuchak_share, 'urdf', 'cuchak.urdf.xacro')

    rviz_config_path = os.path.join(get_package_share_path('custom_turtlebot_description'),
                                    'rviz', 'config.rviz')

    gz_sim_path = os.path.join(get_package_share_path('ros_gz_sim'),
                               'launch', 'gz_sim.launch.py')

    # Para que Gazebo encuentre model://cuchak_description/meshes/...
    set_resource_path = AppendEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH',
        os.path.dirname(str(cuchak_share)))

    robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{'robot_description': robot_description}]
    )

    gz_sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_sim_path),
        launch_arguments={'gz_args': 'empty.sdf -r -v 4'}.items()
    )

    gz_create_node = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=["-topic", "/robot_description"],
        output="screen"
    )

    rviz2_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d', rviz_config_path]
    )

    return LaunchDescription([
        set_resource_path,          # primero, antes de lanzar Gazebo
        robot_state_publisher_node,
        gz_sim_launch,
        gz_create_node,
        rviz2_node
    ])