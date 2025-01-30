import enum

class Action(enum.Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    STAY = (0, 0)

def get_proba_from_agent(x, y, action, grid_size=4):
    """ Retourne les probabilités de l'action """
    proba = {}

    match action:
        case Action.STAY:
            proba[(x, y)] = 1.0
        case _:
            if is_valid_move(x, y, action.value, grid_size):
                main_x, main_y = x + action.value[0], y + action.value[1]
                proba[(main_x, main_y)] = 0.9
                
                # Définition des mouvements diagonaux
                if action in [Action.UP, Action.DOWN]:
                    left_diag_x, left_diag_y = x - 1, y + action.value[1]
                    right_diag_x, right_diag_y = x + 1, y + action.value[1]
                else:  # Action.LEFT ou Action.RIGHT
                    left_diag_x, left_diag_y = x + action.value[0], y - 1
                    right_diag_x, right_diag_y = x + action.value[0], y + 1
                
                # Vérification et ajustement des probabilités
                left_valid = is_valid_move(x, y, (left_diag_x - x, left_diag_y - y), grid_size)
                right_valid = is_valid_move(x, y, (right_diag_x - x, right_diag_y - y), grid_size)
                
                if left_valid and right_valid:
                    proba[(left_diag_x, left_diag_y)] = 0.05
                    proba[(right_diag_x, right_diag_y)] = 0.05
                elif left_valid:
                    proba[(left_diag_x, left_diag_y)] = 0.1
                elif right_valid:
                    proba[(right_diag_x, right_diag_y)] = 0.1
            else:
                proba[(x, y)] = 1.0  # Si mouvement impossible, on reste sur place
    
    return proba

def get_proba_from_action(init_state, action1, action2, grid_size=4):
    """ Retourne les probabilités de l'action """
    proba = {}

    x1, y1, x2, y2 = state_to_grid(init_state, grid_size)
    probaA1 = get_proba_from_agent(x1, y1, action1, grid_size)
    probaA2 = get_proba_from_agent(x2, y2, action2, grid_size)

    for (x1, y1), p1 in probaA1.items():
        for (x2, y2), p2 in probaA2.items():
            new_state = grid_to_state(x1, y1, x2, y2, grid_size)
            proba[new_state] = p1 * p2

    return proba

def grid_to_state(x1, y1, x2, y2, grid_size=4):
    """ Retourne l'état à partir des positions des agents """
    return x1 * grid_size * grid_size * grid_size + y1 * grid_size * grid_size + x2 * grid_size + y2

def state_to_grid(state, grid_size=4):
    """ Retourne les positions des agents à partir de l'état """
    x1 = state // (grid_size * grid_size * grid_size)
    state = state % (grid_size * grid_size * grid_size)
    y1 = state // (grid_size * grid_size)
    state = state % (grid_size * grid_size)
    x2 = state // grid_size
    y2 = state % grid_size
    return x1, y1, x2, y2

def is_valid_move(x, y, action, grid_size=4):
    """ Retourne si le mouvement est valide """
    return (x + action[0] >= 0 and x + action[0] < grid_size and y + action[1] >= 0 and y + action[1] < grid_size)

def generate_dpomdp_file(filename="grid_large.dpomdp"):
    agents = 2
    discount = 0.9
    grid_size = 4
    init_state = grid_to_state(0, 0, 0, 0, grid_size)
    num_states = grid_size * grid_size * grid_size * grid_size
    observations = ["murDG", "murHB"]
    actions = [Action.UP.name, Action.DOWN.name, Action.LEFT.name, Action.RIGHT.name, Action.STAY.name]

    print(grid_to_state(0, 0, 0, 0, grid_size))
    print(grid_to_state(3, 3, 3, 3, grid_size))
    print(state_to_grid(5, grid_size))

    # example : 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0
    start = ""
    for state in range(num_states):
        if state == init_state:
            start += "1.0 "
        else:
            start += "0.0 "

    with open(filename, "w") as f:
        f.write("agents: {}\n".format(agents))
        f.write("discount: {}\n".format(discount))
        f.write("values: reward\n")
        f.write("states: {}\n".format(num_states))
        f.write("start: \n{}\n".format(start))
        f.write(f"actions:\n{' '.join(actions)}\n{' '.join(actions)}\n")
        f.write(f"observations:\n{' '.join(observations)}\n{' '.join(observations)}\n")

        for state in range(num_states):
            x1, y1, x2, y2 = state_to_grid(state, grid_size)
            for action1 in Action:
                for action2 in Action:
                    proba = get_proba_from_action(state, action1, action2, grid_size)
                    for next_state, p in proba.items():
                        f.write("T: {} {} : {} : {} : {}\n".format(action1.name, action2.name, state, next_state, round(p, 2)))

        for state in range(num_states):
            x1, y1, x2, y2 = state_to_grid(state, grid_size)
            for observation in observations:
                if (x1 == 0 and y1 == 0) or (x2 == 0 and y2 == 0):
                    f.write("O: * : {} : {} : 0.95\n".format(state, observation))
                else:
                    f.write("O: * : {} : {} : 0.05\n".format(state, observation))

        for state in range(num_states):
            x1, y1, x2, y2 = state_to_grid(state, grid_size)
            if (x1 == 0 and y1 == 0) or (x2 == 0 and y2 == 0):
                f.write("R: * : {} : * : * : 1.0\n".format(state))
            else:
                f.write("R: * : {} : * : * : 0.0\n".format(state))

generate_dpomdp_file()
