from copy import deepcopy

from agent.agent import Agent
from constants.constants import *
from random import randrange


class World(object):

    def __init__(self, width: int, height: int):
        assert width > 0, 'World width has to be positive value'
        assert height > 0, 'World height has to be positive value'

        self.__width = width
        self.__height = height
        self.__world = [[EMPTY_FIELD_VALUE for _ in range(width)].copy() for _ in range(height)]
        self.__agent = None
        self.generate_world()

    def generate_world(self):
        self.place_obstacles()

    def place_agent(self, agent: Agent):
        self.__agent = agent
        new_x = randrange(0, self.__width)
        new_y = randrange(0, self.__height)
        self.__agent.set_position(new_x, new_y)
        self.__world[new_y][new_x] = AGENT_VALUE
        self.place_destination()

    def place_destination(self):
        x = randrange(0, self.__width)
        y = randrange(0, self.__height)
        self.__world[y][x] = DESTINATION_VALUE
        self.__agent.set_destination(x, y)

    def place_obstacles(self):
        for _ in range(OBSTACLES_COUNT):
            x = randrange(0, self.__width)
            y = randrange(0, self.__height)
            size = randrange(2, MAX_OBSTACLE_SIZE + 1)
            if self.is_place_suitable(x, y, size):
                self.place_obstacle(x, y, size)

    def is_place_suitable(self, x, y, size):
        for height in range(-(MIN_OBSTACLE_HEIGHT * size) // 2, (MIN_OBSTACLE_HEIGHT * size) // 2):
            for width in range(-(MIN_OBSTACLE_WIDTH * size) // 2, (MIN_OBSTACLE_WIDTH * size) // 2):
                if not (0 <= x + width < self.__width) or not (0 <= y + height < self.__height):
                    return False
                if self.__world[y + height][x + width] != EMPTY_FIELD_VALUE:
                    return False
        return True

    def place_obstacle(self, x, y, size):
        for height in range(-(MIN_OBSTACLE_HEIGHT * size) // 2, (MIN_OBSTACLE_HEIGHT * size) // 2):
            for width in range(-(MIN_OBSTACLE_WIDTH * size) // 2, (MIN_OBSTACLE_WIDTH * size) // 2):
                self.__world[y + height][x + width] = OBSTACLE_VALUE

    def get_point_environment_vector(self, x: int, y: int):
        assert 0 <= x <= self.__width, 'Bad point coordinates'
        assert 0 <= y <= self.__height, 'Bad point coordinates'

        env_vector = [[OBSTACLE_VALUE for _ in range(3)].copy() for _ in range(3)]
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= y + i < self.__height and 0 <= x + j < self.__width:
                    env_vector[i + 1][j + 1] = self.__world[y + i][x + j]
        return env_vector

    def is_field_empty(self, x: int, y: int):
        if 0 <= x < self.__width and 0 <= y < self.__height:
            return self.__world[y][x] == EMPTY_FIELD_VALUE or self.__world[y][x] == DESTINATION_VALUE
        return False

    def update_agent_point(self, past_x: int = None, past_y: int = None, new_x: int = None, new_y: int = None):
        if past_x is None or past_y is None:
            past_x, past_y = self.find_agent()
        if new_x is None or new_y is None:
            current_agent_position = self.__agent.get_position()
            new_x, new_y = current_agent_position[0], current_agent_position[1]
        self.change_field_value(past_x, past_y, EMPTY_FIELD_VALUE)
        self.change_field_value(new_x, new_y, AGENT_VALUE)

    def find_agent(self):
        for y, row in enumerate(self.__world):
            for x, field in enumerate(row):
                if field == AGENT_VALUE:
                    return x, y
        return -1, -1

    def change_field_value(self, x: int, y: int, value):
        if 0 <= x < self.__width and 0 <= y < self.__height:
            self.__world[y][x] = value

    def __str__(self):
        world_as_string = ""
        for world_row in self.__world:
            world_as_string += self.get_world_row_as_string(world_row) + '\n'
        return world_as_string

    def get_world_row_as_string(self, world_row):
        row = ""
        for field in world_row:
            if field == OBSTACLE_VALUE:
                row += OBSTACLE_CHAR
            elif field == DESTINATION_VALUE:
                row += DESTINATION_CHAR
            elif field == AGENT_VALUE:
                row += AGENT_CHAR
            else:
                row += EMPTY_FIELD_CHAR
            row += " "
        return row

    def clear_world(self):
        self.__world = [[EMPTY_FIELD_VALUE for _ in range(self.__width)].copy() for _ in range(self.__height)]

    def set_width(self, width: int):
        assert width > 0, 'World width has to be positive value'
        self.__width = width

    def set_height(self, height: int):
        assert height > 0, 'World height has to be positive value'
        self.__height = height

    def set_world_array(self, world: list[list[int]]):
        self.__world = world

    def get_point(self, x: int, y: int):
        assert 0 <= x < self.__width, 'Point beyond the world'
        assert 0 <= y < self.__height, 'Point beyond the world'
        return self.__world[y][x]

    def get_agent(self):
        return self.__agent

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_world_copy(self):
        return deepcopy(self.__world)

    def place_destination_on_map(self, x, y):
        self.__world[y][x] = DESTINATION_VALUE
        self.__agent.set_destination(x, y)


if __name__ == '__main__':
    test_world = World(20, 20)
    print(test_world)
    print(test_world.get_point_environment_vector(0, 0))
    print(test_world.get_point_environment_vector(5, 5))
    print(test_world.get_point_environment_vector(0, 19))
    print(test_world.get_point_environment_vector(19, 0))
    print(test_world.get_point_environment_vector(19, 19))
