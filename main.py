from constants.constants import OBSTACLE_VALUE, OBSTACLE_CHAR, DESTINATION_VALUE, DESTINATION_CHAR, AGENT_VALUE, AGENT_CHAR, PATH_VALUE, PATH_CHAR, EMPTY_FIELD_CHAR
from world.world import World
from agent.agent import Agent
import matplotlib.pyplot as plt
from time import time


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
    world_height, world_width = 15, 15
    world = World(world_width, world_height)
    agent = Agent(world)
    world.place_agent(agent)
    print(world)
    start_agent_x, start_agent_y = agent.get_position()
    dx, dy = agent.get_destination()
    fail_counter = 0

    learning_count = 1

    for i in range(learning_count):
        start = time()
        while True:
            current_exploration_rate = agent.get_exploration_rate()

            if current_exploration_rate < 0.01:
                optimal_path, path_size = agent.get_optimal_path()
                print("")
                print(agent.get_strategy_bucket())
                print_path(optimal_path)

                import constants
                plt.scatter(constants.constants.EMPTY_FIELD_COST, path_size)
                constants.constants.EMPTY_FIELD_COST += 0.2

                print('learned')
                agent.reset()
                break

            status = agent.go_to_destination()
            if status == 0:
                fail_counter += 1
            if status == 1:
                fail_counter -= 9999999
            if fail_counter > 100:
                raise Exception("bad world")

            agent.learn_new_strategy()
            agent.set_position(start_agent_x, start_agent_y)
            world.place_destination_on_map(dx, dy)
        print(time() - start)
    # plt.show()


if __name__ == '__main__':
    main2()
