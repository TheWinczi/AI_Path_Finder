"""
    File including Agent class which
    implementing methods of moving around,
    making decisions, storing the history of decisions.
"""
import random
from random import randrange
from agent.decision import Decision
from agent.strategyBucket import StrategyBucket
from constants.constants import *
from direction import Direction


class Agent(object):
    """ Class representing agent in game world.
        Agent has to reach to destination point
        in the shortest distance. World is random generated. """

    def __init__(self):
        """ Initialize the Agent """
        self.__history = []
        self.__x = 0
        self.__y = 0
        self.__destination_x = 0
        self.__destination_y = 0
        self.__strategy_bucket = StrategyBucket()
        self.__exploration_rate = EXPLORATION_RATE_INIT
        self.__exploration_decaying_rate = EXPLORATION_DECAY_RATE

    def make_decision(self, environment: list):
        """ make decision where agent have to go """
        direction = Direction.get_direction(randrange(0, 4))
        if random.uniform(0, 1) < self.__exploration_rate:
            self.__exploration_rate *= self.__exploration_decaying_rate
            direction_from_bucket = self.__strategy_bucket.get_strategy(environment)
            if direction_from_bucket is not None:
                direction = direction_from_bucket

        self.move(Decision(direction, environment))

    def move(self, decision: Decision):
        """ Move the agent in a given direction """
        self.__history.append(decision)
        self.__y += decision.direction[0]
        self.__x += decision.direction[1]
        if self.is_in_destination():
            self.give_history_to_strategy_bucket()

    def give_history_to_strategy_bucket(self):
        self.__strategy_bucket.add_strategy(self.__history)

    def is_in_destination(self):
        if self.__x == self.__destination_x and self.__y == self.__destination_y:
            return True
        return False

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

    def set_destination(self, x: int, y: int):
        self.__destination_x = x
        self.__destination_y = y

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
