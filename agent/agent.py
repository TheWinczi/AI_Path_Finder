import random
from random import randrange
from agent.decision import Decision
from agent.strategyBucket import StrategyBucket
from constants.constants import *
from direction import Direction


class Agent(object):
    """ Class representing agent in game world.
        Agent has to reach to destination point
        in the shortest distance """

    def __init__(self, world):
        self.__coords_history = []
        self.__world = world
        self.__history = []
        self.__x = 0
        self.__y = 0
        self.__start_x = -1
        self.__start_y = -1
        self.__destination_x = 0
        self.__destination_y = 0
        self.__strategy_bucket = StrategyBucket()
        self.__exploration_rate = EXPLORATION_RATE_INIT
        self.__exploration_decaying_rate = EXPLORATION_DECAY_RATE

    def make_decision(self, environment: list):
        direction = self.choose_direction()
        if random.uniform(0, 1) > self.__exploration_rate:
            direction_from_bucket = self.__strategy_bucket.get_strategy(environment)
            if direction_from_bucket is not None:
                direction = direction_from_bucket.direction
        return Decision(environment, direction)

    def move(self, decision: Decision):
        past_x, past_y = self.__x, self.__y
        self.__y += decision.direction.value[0]
        self.__x += decision.direction.value[1]
        self.add_to_history(decision)
        self.__world.update_agent_point(past_x, past_y, self.__x, self.__y)

    def go_to_destination(self, max_moves: int = MAX_AGENT_MOVES_COUNT):
        self.__start_x, self.__start_y = self.__x, self.__y
        for _ in range(max_moves):
            decision = self.make_decision(self.__world.get_point_environment_vector(self.__x, self.__y))
            self.move(decision)
            if self.is_in_destination():
                return 1
        return 0

    def learn_new_strategy(self):
        self.give_history_to_strategy_bucket()
        self.__strategy_bucket.learn_using_history(self.is_in_destination())
        self.__exploration_rate *= self.__exploration_decaying_rate
        self.clear_history()

    def choose_direction(self):
        counter = 0
        while counter := counter + 1:
            direction = Direction.get_direction(randrange(0, 4))
            if self.__world.is_field_empty(self.__x + direction.value[1], self.__y + direction.value[0]):
                return direction
            if counter > 10000:
                raise Exception("bad world")

    def give_history_to_strategy_bucket(self):
        self.__strategy_bucket.add_new_decisions_history(self.__history)

    def is_in_destination(self):
        if self.__x == self.__destination_x and self.__y == self.__destination_y:
            return True
        return False

    def add_to_history(self, decision: Decision):
        self.__history.append(decision)
        self.__coords_history.append((self.__x, self.__y))

    def __str__(self):
        string_agent = "{"
        string_agent += "position: (" + str(self.__x) + ", " + str(self.__y) + ")"
        string_agent += " | "
        string_agent += "destination: (" + str(self.__destination_x) + ", " + str(self.__destination_y) + ")"
        string_agent += "}"
        return string_agent

    def reset(self):
        self.__history.clear()
        self.__coords_history.clear()
        self.__exploration_rate = EXPLORATION_RATE_INIT
        self.__exploration_decaying_rate = EXPLORATION_DECAY_RATE
        self.go_to_start()

    def reset_strategy_bucket(self):
        self.__strategy_bucket.reset()

    def clear_history(self):
        self.__history.clear()
        self.__coords_history.clear()

    def go_to_start(self):
        self.__x = self.__start_x
        self.__y = self.__start_y
        self.__world.update_agent_point(new_x=self.__x, new_y=self.__y)

    def place_on_world(self, x: int, y: int):
        self.set_position(x, y)
        self.__start_x, self.__start_y = self.__x, self.__y

    def set_position(self, x: int, y: int):
        self.__x = x
        self.__y = y
        self.__world.update_agent_point(new_x=x, new_y=y)

    def set_destination(self, x: int, y: int):
        self.__destination_x = x
        self.__destination_y = y

    def get_destination(self):
        return self.__destination_x, self.__destination_y

    def set_world(self, world):
        self.__world = world

    def get_history(self):
        return self.__history

    def get_position(self):
        return self.__x, self.__y

    def get_start_position(self):
        return self.__start_x, self.__start_y

    def get_strategy_bucket(self):
        return self.__strategy_bucket

    def get_exploration_rate(self):
        return self.__exploration_rate

    def get_coords_history(self):
        return self.__coords_history

    def get_optimal_path(self):
        map = self.__world.get_world_copy()
        self.__exploration_rate = 0
        self.go_to_destination()
        for coord in self.__coords_history:
            if map[coord[1]][coord[0]] != DESTINATION_VALUE and map[coord[1]][coord[0]] != AGENT_VALUE:
                map[coord[1]][coord[0]] = PATH_VALUE
        return map, len(self.__coords_history)


if __name__ == '__main__':
    agent = Agent()
    print(agent)
    agent.add_to_history(Decision([1, 0, 0, 1, 0, 1], 5))
    agent.add_to_history(Decision([1, 0, 2, 3, 5, 6], 5))
    agent.add_to_history(Decision([1, 1, 0, 3, 6, 5], 5))
    print(agent.get_history())
    agent.clear_history()
    print(agent.get_history())
