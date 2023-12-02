def perform_place(instance, action):
    user_input = input(f'\t{action}\twas the action correct? (y/n)')
    action_name = action.action.name
    action_params = [str(params ) for params in action.actual_parameters]

    if not user_input or user_input == '' or user_input == ' ' :
        user_input = 'y'
    if user_input == 'y':
        instance.problem.set_initial_value(instance.fluents_dict['holding'](instance.objects_dict[action_params[0]], instance.objects_dict[action_params[2]]), False)
        instance.problem.set_initial_value(instance.fluents_dict['gripper_is_free'](instance.objects_dict[action_params[0]]), True)
        instance.problem.set_initial_value(instance.fluents_dict['on'](instance.objects_dict[action_params[2]], instance.objects_dict[action_params[1]]), True)
        instance.problem.set_initial_value(instance.fluents_dict['perceived'](instance.objects_dict[action_params[1]]), False)
        return True
    elif user_input == 'N' or user_input == 'n':
        return False