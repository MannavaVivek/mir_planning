from unified_planning.io import PDDLReader, PDDLWriter
from unified_planning.shortcuts import *
from unified_planning.engines import PlanGenerationResultStatus
import unified_planning as up
from rclpy.node import Node
import rclpy
import os
from ament_index_python.packages import get_package_share_directory

from actions.base_insert_action import perform_insert
from actions.move_base_action import perform_move_base
from actions.base_perceive_action import perform_perceive
from actions.base_pick_action import perform_pick
from actions.base_place_action import perform_place
from actions.stage_action import perform_stage
from actions.unstage_action import perform_unstage


class PlannerExecutor(Node):
    def __init__(self):
        super().__init__("planner_executor")
        up.shortcuts.get_environment().credits_stream = None
        self.pddl_reader = PDDLReader()

        self.execution_started = False

        domain_file = os.path.join(
            get_package_share_directory("mir_planning"), "config", "domain.pddl"
        )

        problem_file = os.path.join(
            get_package_share_directory("mir_planning"),
            "config",
            "smaller_problem.pddl",
        )

        self.declare_parameters(
            namespace="",
            parameters=[("domain_path", domain_file), ("problem_path", problem_file)],
        )

        self.domain_path = (
            self.get_parameter("domain_path").get_parameter_value().string_value
        )
        self.problem_path = (
            self.get_parameter("problem_path").get_parameter_value().string_value
        )

        self.problem = self.pddl_reader.parse_problem(
            self.domain_path, self.problem_path
        )
        self.planner = OneshotPlanner(
            problem_kind=self.problem.kind,
            optimality_guarantee=PlanGenerationResultStatus.SOLVED_OPTIMALLY,
        )

        # create a dictionary of fluents and objects to update the initial states
        self.fluents_dict = {}
        for fluent in self.problem.fluents:
            self.fluents_dict[str(fluent.name)] = self.problem.fluent(f"{fluent.name}")

        self.objects_dict = {}
        for obj in self.problem.all_objects:
            self.objects_dict[str(obj.name)] = self.problem.object(f"{obj.name}")

        self.failure_count = {}
        self.goals = []
        self.removed_goals = []

        for goal in self.problem.goals:
            if goal.is_and():
                for g in goal.args:
                    self.goals.append(g)
            else:
                self.goals.append(goal)
        self.problem.clear_goals()

        execution_count = 0
        while execution_count <= 3:
            sorted_goals = []
            is_goals = 0
            for i in range(3):
                is_goals, sorted_goals = self.check_for_goals()
                if is_goals:
                    break
                else:
                    # TODO: should wait for some time?
                    self.get_logger().info(f"Try {i}: No goals to execute. retrying...")

            if is_goals:
                self.execution_started = True
                self.execute(sorted_goals)
            else:
                if self.execution_started:
                    self.get_logger().info(
                        "All goals executed. Waiting for new goals..."
                    )
                    execution_count += 1
                    if len(self.removed_goals) > 0:
                        self.goals = self.removed_goals
                        self.removed_goals = []
                    else:
                        break
                else:
                    self.get_logger().info("Waiting for goals to start execution...")

    def check_for_goals(self):
        if len(self.goals) == 0:
            return (False, [])
        else:
            self.sorted_goals = []
            if len(self.goals) >= 3:
                for i in range(3):
                    self.sorted_goals.append(self.goals[i])
            else:
                for i in range(len(self.goals)):
                    self.sorted_goals.append(self.goals[i])
            return (True, self.sorted_goals)

    def remove_goal_with_object(self, object_name):
        for goal in self.problem.goals:
            goal_str = str(goal)
            if object_name in goal_str:
                self.removed_goals.append(goal)

        self.goals = [goal for goal in self.goals if goal not in self.removed_goals]
        self.problem.clear_goals()

    def remove_goals_with_location(self, location):
        for goal in self.goals:
            goal_str = str(goal)
            if location in goal_str:
                self.removed_goals.append(goal)
        self.goals = [goal for goal in self.goals if location not in self.removed_goals]
        # TODO: doing it with removed goals for now. might cause issues in retries
        self.problem.clear_goals()

    def remove_successful_goals(self):
        self.goals = [goal for goal in self.goals if goal not in self.problem.goals]
        self.problem.clear_goals()

    def execute(self, goals):
        self.get_logger().info("Executing goals...")
        self.problem.clear_goals()
        for goal in goals:
            self.get_logger().info(f"\t{goal}")
            self.problem.add_goal(goal)
        self.plan = self.planner.solve(self.problem).plan.actions
        result = True
        for idx, action in enumerate(self.plan):
            action_name = action.action.name

            if action_name == "move_base":  # TODO: need to organize this     better
                result = perform_move_base(self, action)
            elif action_name == "perceive":
                if idx + 1 < len(self.plan) and (
                    self.plan[idx + 1].action.name == "pick"
                    or self.plan[idx + 1].action.name == "PICK"
                ):
                    pick_params = [
                        str(params) for params in self.plan[idx + 1].actual_parameters
                    ]
                    result = perform_perceive(self, action, pick_params[2])
                else:
                    result = perform_perceive(
                        self, action, "mystery_object"
                    )  # if it came to this, something went very wrong
            elif action_name == "pick":
                result = perform_pick(self, action)
            elif action_name == "stage_general" or action_name == "stage_large":
                result = perform_stage(self, action)
            elif action_name == "unstage":
                result = perform_unstage(self, action)
            elif action_name == "place":
                result = perform_place(self, action)
            elif action_name == "insert":
                result = perform_insert(self, action)

            if not result:
                break

        if result:
            self.remove_successful_goals()


def main():
    rclpy.init()
    planner_executor = PlannerExecutor()
    rclpy.spin(planner_executor)
    planner_executor.destroy_node()
    rclpy.shutdown()
