def perform_place(instance, action):
    user_input = input(f'\t{action}\twas the action correct? (y/n)')
    action_name = action.action.name
    action_params = [str(params) for params in action.actual_parameters]
    robot = str(action.actual_parameters[0])
    location = str(action.actual_parameters[1])
    object = str(action.actual_parameters[2])
    if not user_input or user_input == '' or user_input == ' ' :
        user_input = 'y'
    if user_input == 'y':
        instance.problem.set_initial_value(instance.fluents_dict['holding'](instance.objects_dict[robot], instance.objects_dict[object]), False)
        instance.problem.set_initial_value(instance.fluents_dict['gripper_is_free'](instance.objects_dict[robot]), True)
        instance.problem.set_initial_value(instance.fluents_dict['on'](instance.objects_dict[object], instance.objects_dict[location]), True)
        instance.problem.set_initial_value(instance.fluents_dict['perceived'](instance.objects_dict[location]), False)
        return True
    elif user_input == 'N' or user_input == 'n':
        instance.get_logger().warn(f"Place failed for {object}.")
        instance.get_logger().warn("And yet, nothing is changed in KB") #TODO : need to deal with this, but how?
        return False