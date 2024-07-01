import os

from ament_index_python.packages import get_package_share_directory

from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch.actions import ExecuteProcess
import xacro

def generate_static_tf_publisher_node(parentFrame, childFrame):
    return Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name=f"static_tf_publisher_{parentFrame}",
        arguments=["0", "0", "0", "0", "0", "0", parentFrame, childFrame],
        parameters=[{"use_sim_time": True}],
    )

def generate_launch_description():

    
    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='testbot' #<--- CHANGE ME

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    gazebo = ExecuteProcess(
            cmd=['ign', 'gazebo','src/testbot/worlds/obstacle.sdf'],
            output='screen'
        )


    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='ros_gz_sim', executable='create',
                        arguments=['-topic', 'robot_description'],
                        output='screen')

    # control_node = Node(
    #     package="controller_manager",
    #     executable="ros2_control_node",
    #     parameters=[xacro_file, controller_config_path],
    #     output='both',
    #     )
    

    # diff_drive_spawner = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["diff_cont"],
    #     output="both",
    # )

    # joint_broad_spawner = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["joint_broad","--controller-manager", "/controller_manager"],
    #     output="both",
    # )
    
    # diff_drive_spawner=ExecuteProcess(
    #     cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
    #          'diff_cont'],
    #     output='screen'
    # )
        
    # joint_broad_spawner=ExecuteProcess(
    #     cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
    #          'joint_broad'],
    #     output='screen'
    # )


    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{"use_sim_time": True}],
        arguments=[#'/device/imu/data@sensor_msgs/msg/Imu@ignition.msgs.IMU',
                   #'/navsat/fix@sensor_msgs/msg/NavSatFix@ignition.msgs.NavSat',
                   #'/rgbd/camera/depth_image@sensor_msgs/msg/Image@ignition.msgs.Image',
                   #'/rgbd/camera/camera_info@sensor_msgs/msg/CameraInfo@ignition.msgs.CameraInfo',
                   #'/rgbd/camera/points@sensor_msgs/msg/PointCloud2@ignition.msgs.PointCloudPacked',
                   #'/rgbd/camera/image@sensor_msgs/msg/Image@ignition.msgs.Image',
                   '/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist',
                   '/odometry@nav_msgs/msg/Odometry[ignition.msgs.Odometry',
                   '/joint_state@sensor_msgs/msg/JointState[ignition.msgs.Model',
                   #'/odom@nav_msgs/msg/Odometry@ignition.msgs.OdometryWithCovariance',
                   #'/sensor_msgs/msg/JointState	gz.msgs.Model',
                   '/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V',
                   '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock',
                   '/scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan'
                   ],
        output="screen"
    )

    # Launch them all!
    return LaunchDescription([
    
        bridge,
        rsp,
        gazebo,
        spawn_entity,
        # # control_node,
        # RegisterEventHandler(
        #     event_handler=OnProcessExit(
        #         target_action=spawn_entity,
        #         on_exit=[joint_broad_spawner],
        #     )
        # ),
        # RegisterEventHandler(
        #     event_handler=OnProcessExit(
        #         target_action=joint_broad_spawner,
        #         on_exit=[diff_drive_spawner],
        #     )
        # ),

    ])