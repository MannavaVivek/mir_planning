def perform_move_base(instance, action):
    user_input = input(f'\t{action}\twas the action correct? (y/n)')
    action_name = action.action.name
    action_params = [str(params ) for params in action.actual_parameters]
    robot = str(action.actual_parameters[0])
    source_location = str(action.actual_parameters[1])
    destination_location = str(action.actual_parameters[2])

    if not user_input or user_input == '' or user_input == ' ' :
        user_input = 'y'
    if user_input == 'y':
        instance.problem.set_initial_value(instance.fluents_dict['at'](instance.objects_dict[robot], instance.objects_dict[source_location]), False)
        instance.problem.set_initial_value(instance.fluents_dict['at'](instance.objects_dict[robot], instance.objects_dict[destination_location]), True)
        instance.problem.set_initial_value(instance.fluents_dict['perceived'](instance.objects_dict[source_location]), False)
        instance.problem.set_initial_value(instance.fluents_dict['perceived'](instance.objects_dict[destination_location]), False)
        return True
    elif user_input == 'N' or user_input == 'n':
        if destination_location in instance.failure_count.keys():
            instance.failure_count[destination_location] += 1
            #TODO: should consider the position change to start ?
        else:
            instance.failure_count[destination_location] = 1
        count = instance.failure_count[destination_location]
        if count > 2:
            instance.remove_goals_with_location(destination_location)
            instance.get_logger().warn(f"Moving to {destination_location} failed {count}times. Removing all goals on this workstation.")
        return False