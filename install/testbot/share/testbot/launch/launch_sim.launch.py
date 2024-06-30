import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch.actions import ExecuteProcess

def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='testbot' #<--- CHANGE ME

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )


    # # Declare the launch argument for the world file, 'empty.sdf' loaded at default.
    # # Add world:=/path/to/desired/worldfile for manual world file selection.

    

    # Include the Gazebo launch file, provided by the gazebo_ros package
    # gazebo = IncludeLaunchDescription(
    #             PythonLaunchDescriptionSource([os.path.join(
    #                 get_package_share_directory('ign_gazebo'), 'launch', 'gazebo.launch.py')]),
    #          )

    gazebo = ExecuteProcess(
            cmd=['ign', 'gazebo','src/testbot/worlds/obstacle.sdf'],
            output='screen'
        )
    
    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='ros_gz_sim', executable='create',
                        arguments=['-topic', 'robot_description'],
                        output='screen')

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont","--controller-manager", "/controller_manager"],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad","--controller-manager", "/controller_manager"],
    )
    


    # Launch them all!
    return LaunchDescription([
        rsp,
        
        # declare_world_cmd,
        gazebo,
        spawn_entity,
        diff_drive_spawner,
        joint_broad_spawner

    ])