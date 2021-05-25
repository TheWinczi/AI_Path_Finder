from constants.constants import OBSTACLE_VALUE, OBSTACLE_CHAR, DESTINATION_VALUE, DESTINATION_CHAR, AGENT_VALUE, AGENT_CHAR, PATH_VALUE, PATH_CHAR, EMPTY_FIELD_CHAR
from world.world import World
from agent.agent import Agent
from gui_app.application import Application


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

    app = Application(world, agent)
    app.start()


if __name__ == '__main__':
    main2()
