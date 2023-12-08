def perform_insert(instance, action):
    """
    performs the insert action and returns success message
    """
    user_input = input(f'\t{action}\twas the action correct? (y/n)')
    action_name = action.action.name
    robot = str(action.actual_parameters[0])
    platform = str(action.actual_parameters[1])
    location = str(action.actual_parameters[2])
    peg = str(action.actual_parameters[3])
    hole = str(action.actual_parameters[4])

    if not user_input or user_input == '' or user_input == ' ' :
        user_input = 'y'
    if user_input == 'y':
        instance.problem.set_initial_value(instance.fluents_dict['in'](instance.objects_dict[peg], instance.objects_dict[hole]), True)
        instance.problem.set_initial_value(instance.fluents_dict['on'](instance.objects_dict[peg], instance.objects_dict[location]), True)
        instance.problem.set_initial_value(instance.fluents_dict['heavy'](instance.objects_dict[peg]), True)
        instance.problem.set_initial_value(instance.fluents_dict['heavy'](instance.objects_dict[hole]), True)
        instance.problem.set_initial_value(instance.fluents_dict['stored'](instance.objects_dict[platform], instance.objects_dict[peg]), False)
        instance.problem.set_initial_value(instance.fluents_dict['occupied'](instance.objects_dict[platform]), False)
        return True
    elif user_input == 'N' or user_input == 'n':
        if peg in instance.failure_count.keys():
            instance.failure_count[peg] += 1
        else:
            instance.failure_count[peg] = 1
        count = instance.failure_count[peg]
        if count > 2:
            #TODO : need to deal with this failure to insert 
            instance.get_logger().warn(f" Insert failed for {peg} {count} times")
            instance.problem.set_initial_value(instance.fluents_dict['at'](instance.objects_dict[robot], instance.objects_dict[location]), False)
            instance.problem.set_initial_value(instance.fluents_dict['at'](instance.objects_dict[robot], instance.objects_dict["start"]), True)
            instance.failure_count[peg] = 1
        return False