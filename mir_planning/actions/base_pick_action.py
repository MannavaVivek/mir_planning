def perform_pick(instance, action):
    user_input = input(f'\t{action}\twas the action correct? (y/n)')
    action_name = action.action.name
    action_params = [str(params ) for params in action.actual_parameters]

    if not user_input or user_input == '' or user_input == ' ' :
        user_input = 'y'
    if user_input == 'y':
        instance.problem.set_initial_value(instance.fluents_dict['on'](instance.objects_dict[action_params[2]], instance.objects_dict[action_params[1]]), False)
        instance.problem.set_initial_value(instance.fluents_dict['gripper_is_free'](instance.objects_dict[action_params[0]]), False)
        instance.problem.set_initial_value(instance.fluents_dict['holding'](instance.objects_dict[action_params[0]], instance.objects_dict[action_params[2]]), True)
        return True
    elif user_input == 'N' or user_input == 'n':
        if action_params[2] in instance.failure_count.keys():
            instance.failure_count[action_params[2]] += 1
        else:
            instance.failure_count[action_params[2]] = 1
        count = instance.failure_count[action_params[2]]
        if count == 1:
            instance.problem.set_initial_value(instance.fluents_dict['perceived'](instance.objects_dict[action_params[1]]), False)
            print("pick fail count 1")
        elif count == 2:
            print("pick fail count 2")
            instance.problem.set_initial_value(instance.fluents_dict['perceived'](instance.objects_dict[action_params[1]]), False)
            instance.problem.set_initial_value(instance.fluents_dict['at'](instance.objects_dict[action_params[0]], instance.objects_dict[action_params[1]]), False)
            instance.problem.set_initial_value(instance.fluents_dict['at'](instance.objects_dict[action_params[0]], instance.objects_dict["start"]), True)
        elif count == 3:
            print("pick fail count 3")
            instance.problem.set_initial_value(instance.fluents_dict['perceived'](instance.objects_dict[action_params[1]]), False)
            instance.remove_goal_with_object(action_params[2])
            instance.failure_count[action_params[2]] = 0
        return False