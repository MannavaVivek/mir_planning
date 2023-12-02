import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    domain_file = os.path.join(
        get_package_share_directory('mir_planning'),
        'config',
        'domain.pddl'
        )
    
    problem_file = os.path.join(
        get_package_share_directory('mir_planning'),
        'config',
        'smaller_problem.pddl'
        )
        
    node=Node(
        package = 'mir_planning',
        name = 'mir_planner_executor',
        executable = 'mir_planner_executor',
        parameters = [{"domain_path": domain_file}, {"problem_path": problem_file}],
    )

    ld.add_action(node)
    return ld