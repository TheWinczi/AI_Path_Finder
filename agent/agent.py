"""
    File including Agent class which
    implementing methods of moving around,
    making decisions, storing the history of decisions.
"""


class Agent(object):
    """ Class representing agent in game world.
        Agent has to reach to destination point
        in the shortest distance. World is random generated. """

    def __init__(self):
        """ Initialize the Agent """
        self.__history = []
        self.__x = -1
        self.__y = -1
        self.__destination_x = -1
        self.__destination_y = -1

    # ---------
    #   TO DO
    # ---------
    def make_decision(self):
        """ make decision where agent have to go """
        pass

    # ---------
    #   TO DO
    # ---------
    def move(self, way: int):
        """ Move the agent in a given direction """
        pass

    def add_to_history(self, env_vector: list[int], decision: int):
        """ Add new pair of environment vector and decision to history """
        self.__history.append((env_vector, decision))

    def __str__(self):
        """ define how agent should be shown as string """
        string_agent = "{"
        string_agent += "position: (" + str(self.__x) + ", " + str(self.__y) + ")"
        string_agent += " | "
        string_agent += "destination: (" + str(self.__destination_x) + ", " + str(self.__destination_y) + ")"
        string_agent += "}"
        return string_agent

    def set_position(self, x: int, y: int):
        """ Set new agent position """
        self.__x = x
        self.__y = y

    def clear_history(self):
        """ clear agent history """
        self.__history.clear()

    def get_history(self):
        """ Return agent history """
        return self.__history

    def get_position(self):
        """ Return agent position as a tuple (x, y) """
        return self.__x, self.__y


if __name__ == '__main__':
    agent = Agent()
    print(agent)
    agent.add_to_history([1, 0, 0, 1, 0, 1], 5)
    agent.add_to_history([1, 0, 2, 3, 5, 6], 5)
    agent.add_to_history([1, 1, 0, 3, 6, 5], 5)
    print(agent.get_history())
    agent.clear_history()
    print(agent.get_history())
