def perform_insert(instance, action):
    """
    performs the insert action and returns success message
    """
    user_input = input(f'\t{action}\twas the action correct? (y/n)')
    action_name = action.action.name
    action_params = [str(params ) for params in action.actual_parameters]

    if not user_input or user_input == '' or user_input == ' ' :
        user_input = 'y'
    if user_input == 'y':
        instance.problem.set_initial_value(instance.fluents_dict['in'](instance.objects_dict[action_params[3]], instance.objects_dict[action_params[4]]), True)
        instance.problem.set_initial_value(instance.fluents_dict['on'](instance.objects_dict[action_params[3]], instance.objects_dict[action_params[2]]), True)
        instance.problem.set_initial_value(instance.fluents_dict['heavy'](instance.objects_dict[action_params[3]]), True)
        instance.problem.set_initial_value(instance.fluents_dict['heavy'](instance.objects_dict[action_params[4]]), True)
        instance.problem.set_initial_value(instance.fluents_dict['stored'](instance.objects_dict[action_params[1]], instance.objects_dict[action_params[3]]), False)
        instance.problem.set_initial_value(instance.fluents_dict['occupied'](instance.objects_dict[action_params[1]]), False)
        return True
    elif user_input == 'N' or user_input == 'n':
        return False