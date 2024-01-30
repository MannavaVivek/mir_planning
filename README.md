# mir_planning Package

The `mir_planning` package provides planning capabilities using the Unified Planning Framework (UPF) and ROS2. It includes two nodes: `mir_planner_executor` and `mir_planner_executor_lifecycle.py`, both utilizing the UPF for generating plans. The UPF documentation is available at [Unified Planning Framework Docs](https://unified-planning.readthedocs.io/en/latest/).

## Nodes Description

### mir_planner_executor

- **Functionality**: This node generates and executes plans based on provided domain and problem files.
- **Mock Execution**: Currently implemented as a mock run, where the user manually inputs the success or failure of each action in the plan via terminal interaction.
- **Goal Handling**: Goals are extracted from `problem.pddl`, sorted, and fed in batches of three to the planner. Upon completion or failure, the next set of goals is fetched.
- **Failure Handling**: Failed goals are added to a separate list for subsequent execution at the end.

### mir_planner_executor_lifecycle

- **Lifecycle Stages**: Divided into configuring and active states. In the configuring state, it waits for PDDL files. The active state starts the timer callback and execution process.
- **Lifecycle Commands**: Control the node using ROS2 lifecycle commands:
  - `ros2 lifecycle set /planner_executor configure`
  - `ros2 lifecycle set /planner_executor activate`
  - `ros2 lifecycle set /planner_executor deactivate`
  - `ros2 lifecycle set /planner_executor cleanup`
  - `ros2 lifecycle set /planner_executor shutdown`

## Configuration

Both nodes require a domain and a problem file, typically located in `mir_planning/config`. Custom files can be passed as arguments.

## Launch File

A launch file is provided to start the normal version of the node. However, due to the reliance on user text input in the current implementation, its utility is limited.

## Installation and Running

Ensure that you have ROS2 and the Unified Planning Framework installed.

1. Clone the repository into your ROS2 workspace src directory `git clone https://github.com/MannavaVivek/mir_planning.git`.
2. Build the package using `colcon build --symlink-install --packages-select mir_planning`.
3. Source the setup script.
4. Run the node with:
   - `ros2 run mir_planning mir_planner_executor --ros-args -p domain:=<path_to_domain_file> -p problem:=<path_to_problem_file>`
   - Use the launch file for the non-lifecycle version with `ros2 launch mir_planning mir_planner_launch.py`.

## Dependencies

- ROS2
- Unified Planning Framework (UPF)

## Contributing

Contributions to improve the implementation or extend the functionalities of `mir_planning` are welcome. Please follow the standard ROS2 contribution guidelines.

## Author

Vivek Mannava, b-it-bots, H-BRS
