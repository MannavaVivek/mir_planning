def perform_move_base(instance, action):
    user_input = input(f'\t{action}\twas the action correct? (y/n)')
    action_name = action.action.name
    action_params = [str(params ) for params in action.actual_parameters]

    if not user_input or user_input == '' or user_input == ' ' :
        user_input = 'y'
    if user_input == 'y':
        instance.problem.set_initial_value(instance.fluents_dict['at'](instance.objects_dict[action_params[0]], instance.objects_dict[action_params[1]]), False)
        instance.problem.set_initial_value(instance.fluents_dict['at'](instance.objects_dict[action_params[0]], instance.objects_dict[action_params[2]]), True)
        instance.problem.set_initial_value(instance.fluents_dict['perceived'](instance.objects_dict[action_params[1]]), False)
        instance.problem.set_initial_value(instance.fluents_dict['perceived'](instance.objects_dict[action_params[2]]), False)
        return True
    elif user_input == 'N' or user_input == 'n':
        if action_params[2] in instance.failure_count.keys():
            instance.failure_count[action_params[2]] += 1
            #TODO: should consider the position change to start ?
        else:
            instance.failure_count[action_params[2]] = 1
        count = instance.failure_count[action_params[2]]
        if count > 2:
            instance.remove_goals_with_location(action_params[2])
            instance.get_logger().warn(f"Moving to {action_params[2]} failed {count}times. Removing all goals on this workstation.")
        return False