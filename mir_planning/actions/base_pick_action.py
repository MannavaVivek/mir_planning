def perform_pick(instance, action):
    user_input = input(f'\t{action}\twas the action correct? (y/n)')
    action_name = action.action.name
    action_params = [str(params ) for params in action.actual_parameters]
    robot = str(action.actual_parameters[0])
    location = str(action.actual_parameters[1])
    object = str(action.actual_parameters[2])

    if not user_input or user_input == '' or user_input == ' ' :
        user_input = 'y'
    if user_input == 'y':
        instance.problem.set_initial_value(instance.fluents_dict['on'](instance.objects_dict[object], instance.objects_dict[location]), False)
        instance.problem.set_initial_value(instance.fluents_dict['gripper_is_free'](instance.objects_dict[robot]), False)
        instance.problem.set_initial_value(instance.fluents_dict['holding'](instance.objects_dict[robot], instance.objects_dict[object]), True)
        return True
    elif user_input == 'N' or user_input == 'n':
        if object in instance.failure_count.keys():
            instance.failure_count[object] += 1
        else:
            instance.failure_count[object] = 1
        count = instance.failure_count[object]
        if count == 1:
            instance.problem.set_initial_value(instance.fluents_dict['perceived'](instance.objects_dict[location]), False)
            print("pick fail count 1")
        elif count == 2:
            print("pick fail count 2")
            instance.problem.set_initial_value(instance.fluents_dict['perceived'](instance.objects_dict[location]), False)
            instance.problem.set_initial_value(instance.fluents_dict['at'](instance.objects_dict[robot], instance.objects_dict[location]), False)
            instance.problem.set_initial_value(instance.fluents_dict['at'](instance.objects_dict[robot], instance.objects_dict["start"]), True)
        elif count == 3:
            print("pick fail count 3")
            instance.problem.set_initial_value(instance.fluents_dict['perceived'](instance.objects_dict[location]), False)
            instance.remove_goal_with_object(object)
            instance.failure_count[object] = 0
        return False