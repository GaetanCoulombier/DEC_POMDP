# Script to generate a DEC-POMDP file for a 4x4 grid problem

def generate_dpomdp():
    grid_size = 4
    states = grid_size * grid_size
    joint_states = states * states  # Since two robots are involved
    actions = ["up", "down", "left", "right", "stay"]
    observations = ["wall_left", "wall_right"]

    discount = 0.9
    max_reward = 1.0

    def state_to_coordinates(state):
        """Convert state index to grid coordinates."""
        return state // grid_size, state % grid_size

    def coordinates_to_state(x, y):
        """Convert grid coordinates to state index."""
        if 0 <= x < grid_size and 0 <= y < grid_size:
            return x * grid_size + y
        return None  # Invalid coordinates

    def transition_probability(action, start, target):
        """Calculate the transition probability based on action and start/target states."""
        start_x, start_y = state_to_coordinates(start)
        target_x, target_y = state_to_coordinates(target)
        
        if action == "up":
            intended = (start_x - 1, start_y)
        elif action == "down":
            intended = (start_x + 1, start_y)
        elif action == "left":
            intended = (start_x, start_y - 1)
        elif action == "right":
            intended = (start_x, start_y + 1)
        elif action == "stay":
            intended = (start_x, start_y)
        else:
            return 0

        if (target_x, target_y) == intended:
            return 0.9
        elif (target_x, target_y) in [
            (start_x, start_y - 1), (start_x, start_y + 1)
        ]:  # Left or right neighbor
            return 0.05
        return 0

    def observation_probability(observation, state, action):
        """Calculate observation probability."""
        x, y = state_to_coordinates(state)

        if observation == "wall_left" and y == 0:  # Wall on the left
            return 0.95 if action in ["left", "stay"] else 0.1
        elif observation == "wall_right" and y == grid_size - 1:  # Wall on the right
            return 0.95 if action in ["right", "stay"] else 0.1
        return 0.1

    def reward(state_1, state_2, destination):
        """Calculate reward based on distance to destination."""
        x1, y1 = state_to_coordinates(state_1)
        x2, y2 = state_to_coordinates(state_2)
        dx1, dy1 = abs(x1 - destination[0]), abs(y1 - destination[1])
        dx2, dy2 = abs(x2 - destination[0]), abs(y2 - destination[1])
        
        avg_distance = (dx1 + dy1 + dx2 + dy2) / 4.0
        return max_reward - avg_distance / (2 * grid_size - 2)

    with open("Grid4x4.dpomdp", "w") as f:
        f.write("agents: 2\n")
        f.write(f"discount: {discount}\n")
        f.write("values: reward\n")
        f.write(f"states: {joint_states}\n")
        f.write("start:\n")
        f.write(" ".join(["0.0"] * (joint_states - 1) + ["1.0\n"]))

        f.write("actions:\n")
        f.write(" ".join(actions) + "\n")
        f.write(" ".join(actions) + "\n")

        f.write("observations:\n")
        f.write(" ".join(observations) + "\n")
        f.write(" ".join(observations) + "\n")

        for a1 in actions:
            for a2 in actions:
                for s1 in range(states):
                    for s2 in range(states):
                        total_prob = 0.0
                        transitions = []
                        for t1 in range(states):
                            for t2 in range(states):
                                p1 = transition_probability(a1, s1, t1)
                                p2 = transition_probability(a2, s2, t2)
                                prob = p1 * p2
                                if prob > 0:
                                    transitions.append((t1, t2, prob))
                                    total_prob += prob
                        
                        if total_prob > 0:
                            normalization_factor = 1.0 / total_prob
                            for t1, t2, prob in transitions:
                                normalized_prob = prob * normalization_factor
                                f.write(f"T: {a1} {a2} : {s1 * states + s2} : {t1 * states + t2} : {normalized_prob:.6f}\n")

        for o1 in observations:
            for o2 in observations:
                for s1 in range(states):
                    for s2 in range(states):
                        for a1 in actions:
                            for a2 in actions:
                                p1 = observation_probability(o1, s1, a1)
                                p2 = observation_probability(o2, s2, a2)
                                if p1 > 0 and p2 > 0:
                                    f.write(f"O: {a1} {a2} : {s1 * states + s2} : {o1} {o2} : {p1 * p2:.6f}\n")

        destination = (grid_size - 1, grid_size - 1)
        for s1 in range(states):
            for s2 in range(states):
                reward_value = reward(s1, s2, destination)
                f.write(f"R: * : * : {s1 * states + s2} : * : {reward_value:.6f}\n")

if __name__ == "__main__":
    generate_dpomdp()
