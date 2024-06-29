import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import ExecuteProcess

def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='testbot' #<--- CHANGE ME

    # Declare the launch argument for the world file
    declare_world_cmd = DeclareLaunchArgument(
        'world',
        default_value=os.path.join(
            get_package_share_directory(package_name), 'worlds', 'world_demo.sdf'),
        description='Full path to the world file to load'
    )

    # Get the launch configuration for the world file
    world_file = LaunchConfiguration('world')
    # diff_drive_spawner = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["diff_cont"],
    # )

    # joint_broad_spawner = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["joint_broad"],
    # )

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Include the Gazebo launch file, provided by the gazebo_ros package
    # gazebo = IncludeLaunchDescription(
    #             PythonLaunchDescriptionSource([os.path.join(
    #                 get_package_share_directory('ign_gazebo'), 'launch', 'gazebo.launch.py')]),
    #          )

    gazebo = ExecuteProcess(
            cmd=['ign', 'gazebo',world_file],
            output='screen'
        )
    
    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='ros_gz_sim', executable='create',
                        arguments=['-topic', 'robot_description'],
                        output='screen')


    


    # Launch them all!
    return LaunchDescription([
        rsp,
        gazebo,
        declare_world_cmd,
        # diff_drive_spawner,
        # joint_broad_spawner,
        spawn_entity,

    ])