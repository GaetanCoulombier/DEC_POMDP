import enum

class Action(enum.Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    STAY = (0, 0)

def get_proba_from_action(init_state, action, grid_size=4):
    """ Retourne les probabilités de l'action """
    proba = {}

    # 1 when stay
    match action:
        case Action.STAY:
            proba[init_state] = 1
        case _:
            x1, y1, x2, y2 = state_to_grid(init_state, grid_size)
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

def generate_dpomdp_file(filename="GridLarge.dpomdp"):
    agents = 2
    discount = 0.9
    grid_size = 4
    num_states = grid_size * grid_size * grid_size * grid_size
    observations = ["murDG", "murHB"]

    print(grid_to_state(0, 0, 0, 0, grid_size))
    print(grid_to_state(3, 3, 3, 3, grid_size))
    print(state_to_grid(0, grid_size))
    print(state_to_grid(255, grid_size))
    print(is_valid_move(0, 0, Action.UP.value, grid_size))
    

generate_dpomdp_file()
