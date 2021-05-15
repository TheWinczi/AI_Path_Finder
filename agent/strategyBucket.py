from agent.decision import Decision
from constants.constants import *
from math import sqrt


class StrategyBucket(object):

    def __init__(self):
        self.__decisions = []
        self.__strategy = []
        self.__learning_rate = LEARNING_RATE
        self.__discount_rate = DISCOUNT_RATE

    """
    def add_strategy(self, strategy: list):
        strategy_length = len(strategy)
        for decision in strategy:
            decision.rating = self.calculate_decision_rating(decision, strategy_length)
    """

    def add_new_decisions_history(self, history: list[Decision]):
        self.__decisions = history.copy()

    def learn_using_history(self, destination_x: int, destination_y: int, start_x: int, start_y: int):
        for decision in self.__decisions:
            decision_rating = self.calculate_decision_rating(decision, destination_x, destination_y, start_x, start_y)
            self.update_strategy(decision, decision_rating)
            start_x = start_x + decision.direction.value[1]
            start_y = start_y + decision.direction.value[0]

    def update_strategy(self, decision: Decision, value: int):
        index = self.index(decision)
        if index is None:
            self.__strategy.append(decision)
            index = len(self.__strategy)-1
        self.__strategy[index].rating += value

    def get_distance(self, x1: int, y1: int, x2: int, y2: int):
        return sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def index(self, decision: Decision):
        for i, dec in enumerate(self.__strategy):
            if dec.environment == decision.environment and dec.direction == decision.direction:
                return i
        return None

    def calculate_decision_rating(self, decision, destination_x: int, destination_y: int, start_x: int, start_y: int):
        distance_before_decision = self.get_distance(start_x, start_y, destination_x, destination_y)
        distance_after_decision = self.get_distance(start_x + decision.direction.value[1], start_x + decision.direction.value[0], destination_x, destination_y)
        if distance_after_decision < distance_before_decision:
            return 1
        return -0.5

    def get_strategy(self, environment: list):
        decisions_list = self.get_environmental_decisions(environment)
        if len(decisions_list) > 0:
            return self.get_the_best_decision(decisions_list).direction
        return None

    def get_environmental_decisions(self, environment: list):
        decisions_list = []
        for decision in self.__decisions:
            if decision.environment == environment:
                decisions_list.append(decision)
        return decisions_list

    def get_the_best_decision(self, decisions_list: list[Decision]):
        best_decision_rating = decisions_list[0].rating
        best_decision_index = 0
        for i, decision in enumerate(decisions_list):
            if decision.rating > best_decision_rating:
                best_decision_index = i
                best_decision_rating = decision.rating
        return decisions_list[best_decision_index]

    def calculate_q_value(self, current_decision: Decision, new_decision: Decision):
        # todo
        pass

    def calculate_new_strategy(self, current_decision: Decision, new_decision: Decision):
        # TODO new improving strategy - calculate Q-Value
        self.__decisions.remove(current_decision)
        self.__decisions.append(new_decision)

    def __str__(self):
        message = ""
        for decision in self.__strategy:
            message += "[" + str(decision.environment) + " " + str(decision.direction) + " " + str(decision.rating) + "]\n"
        return message
