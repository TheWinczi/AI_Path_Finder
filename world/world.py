"""
    File including World class which
    implementing methods useful for
    handling and building the game world
"""

from constants.constants import *
from random import random, randrange


class World(object):
    """ Class representing world in game """

    def __init__(self, width: int, height: int):
        """ Initialize the world
            @:param width -> width of the world
            @:param height -> height of the world """

        assert width > 0, 'World width has to be positive value'
        assert height > 0, 'World height has to be positive value'

        self.__width = width
        self.__height = height
        self.__world = [[EMPTY_FIELD_VALUE for i in range(width)].copy() for i in range(height)]
        self.__agent_x = 0
        self.__agent_y = 0

        self.generate_world()

    def generate_world(self):
        """ generate random world with the agent, obstacles and target point """
        agent_x = randrange(0, self.__width)
        agent_y = randrange(0, self.__height)
        self.__world[agent_y][agent_x] = AGENT_FIELD_VALUE

        for i in range(OBSTACLES_COUNT):
            obstacle_x = randrange(0, self.__width)
            obstacle_y = randrange(0, self.__height)

            for h in range(-MAX_OBSTACLE_HEIGHT//2, MAX_OBSTACLE_HEIGHT//2):
                for w in range(-MAX_OBSTACLE_WIDTH//2, MAX_OBSTACLE_WIDTH//2):
                    if 0 <= obstacle_x + w < self.__width and 0 <= obstacle_y + h < self.__height:
                        if random() >= OBSTACLE_PROBABILITY and self.__world[obstacle_y+h][obstacle_x+w] == EMPTY_FIELD_VALUE:
                            self.__world[obstacle_y + h][obstacle_x + w] = OBSTACLE_FIELD_VALUE

        destination_x = randrange(0, self.__width)
        destination_y = randrange(0, self.__height)
        self.__world[destination_y][destination_x] = DESTINATION_FIELD_VALUE


    def get_environment_vector(self, x: int, y: int):
        """ Return vector of values representing environment around the point (x, y)"""
        assert 0 <= x <= self.__width, 'Bad point coordinates'
        assert 0 <= y <= self.__height, 'Bad point coordinates'

        env_vector = [OBSTACLE_FIELD_VALUE for i in range(9)]

        if y - 1 >= 0:
            for i in range(-1, 2, 1):
                if 0 <= x + i < self.__width:
                    env_vector[i + 1] = self.__world[y - 1][x + i]

        for i in range(-1, 2, 1):
            if 0 <= x + i < self.__width:
                env_vector[i + 4] = self.__world[y][x + i]

        if y + 1 < self.__height:
            for i in range(-1, 2, 1):
                if 0 <= x + i < self.__width:
                    env_vector[i + 7] = self.__world[y + 1][x + i]

        return env_vector

    def __str__(self):
        """ define how world should be shown as string """
        world_as_string = ""
        for world_row in self.__world:
            row = ""
            for field in world_row:
                if field == OBSTACLE_FIELD_VALUE:
                    row += "# "
                elif field == DESTINATION_FIELD_VALUE:
                    row += "$ "
                elif field == AGENT_FIELD_VALUE:
                    row += "A "
                else:
                    row += ". "
            world_as_string += row + '\n'
        return world_as_string

    def set_width(self, width: int):
        """ Set new world width """
        assert width > 0, 'World width has to be positive value'
        self.__width = width

    def set_height(self, height: int):
        """ Set new world width """
        assert height > 0, 'World height has to be positive value'
        self.__height = height

    def set_agent_point(self, point: tuple[int, int]):
        """ Set new agent point coordinates """
        assert 0 <= point[0] < self.__width, 'Agent point has bad coordinates'
        assert 0 <= point[1] < self.__height, 'Agent point has bad coordinates'
        self.__agent_x = point[0]
        self.__agent_y = point[1]

    def get_point(self, x: int, y: int):
        """ Return point from game world """
        assert 0 <= x < self.__width, 'Point beyond the world'
        assert 0 <= y < self.__height, 'Point beyond the world'
        return self.__world[y][x]

    def get_agent_point(self):
        """ Return agent point coordinates as a tuple """
        return self.__agent_x, self.__agent_y

    def get_width(self):
        """ Return world width """
        return self.__width

    def get_height(self):
        """ Return world height """
        return self.__height


if __name__ == '__main__':
    test_world = World(20, 20)
    print(test_world)
    print(test_world.get_environment_vector(5, 5))
    print(test_world.get_environment_vector(0, 0))
    print(test_world.get_environment_vector(19, 19))
    print(test_world.get_environment_vector(0, 19))
    print(test_world.get_environment_vector(19, 0))
