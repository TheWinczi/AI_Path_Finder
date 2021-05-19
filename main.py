from constants.constants import *
from world.world import World
from agent.agent import Agent


def main():
    world_height, world_width = 20, 20
    world = World(world_width, world_height)
    agent = Agent(world)
    world.place_agent(agent)

    start_agent_x, start_agent_y = agent.get_position()
    while True:
        print(world)
        agent.go_to_destination()
        agent.learn_new_strategy()
        print(world)
        print(agent.get_strategy_bucket())
        input("Press enter:")

        agent.set_position(start_agent_x, start_agent_y)


def print_path(optimal_path):
    world_as_string = ""
    for world_row in optimal_path:
        world_as_string += get_path_row_as_string(world_row) + '\n'
    print(world_as_string)


def get_path_row_as_string(world_row):
    row = ""
    for field in world_row:
        if field == OBSTACLE_VALUE:
            row += OBSTACLE_CHAR
        elif field == DESTINATION_VALUE:
            row += DESTINATION_CHAR
        elif field == AGENT_VALUE:
            row += AGENT_CHAR
        elif field == PATH_VALUE:
            row += PATH_CHAR
        else:
            row += EMPTY_FIELD_CHAR
        row += " "
    return row


def main2():
    world_height, world_width = 20, 20
    world = World(world_width, world_height)
    agent = Agent(world)
    world.place_agent(agent)

    start_agent_x, start_agent_y = agent.get_position()

    print(world)
    while True:
        current_exploration_rate = agent.get_exploration_rate()
        print(current_exploration_rate)
        if current_exploration_rate < 0.001:
            optimal_path = agent.get_optimal_path()
            print_path(optimal_path)
            break
        agent.go_to_destination()
        agent.learn_new_strategy()
        agent.set_position(start_agent_x, start_agent_y)


if __name__ == '__main__':
    main2()
