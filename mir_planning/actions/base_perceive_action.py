def perform_perceive(instance, action, object):
    user_input = input(f'\t{action}\twas the action correct? (y/n)')
    action_name = action.action.name
    action_params = [str(params ) for params in action.actual_parameters]

    if not user_input or user_input == '' or user_input == ' ' :
        user_input = 'y'
    if user_input == 'y':
        instance.problem.set_initial_value(instance.fluents_dict['perceived'](instance.objects_dict[action_params[1]]), True)
        return True
    elif user_input == 'N' or user_input == 'n':
        if object in instance.failure_count.keys():
            instance.failure_count[object] += 1
        else:
            instance.failure_count[object] = 1

        instance.problem.set_initial_value(instance.fluents_dict['at'](instance.objects_dict[action_params[0]], instance.objects_dict[action_params[1]]), False)
        instance.problem.set_initial_value(instance.fluents_dict['at'](instance.objects_dict[action_params[0]], instance.objects_dict["start"]), True)
        count = instance.failure_count[object]
        if count > 2:
            instance.get_logger.warn(f" Perceive failed for {object} {count} times")
            instance.remove_goal_with_object(object)
            instance.failure_count[object] = 0
        return False