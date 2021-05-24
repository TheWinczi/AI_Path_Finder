from agent.decision import Decision
from constants.constants import *
from math import sqrt


class StrategyBucket(object):

    def __init__(self):
        self.__decisions = []
        self.__strategy = []
        self.__learning_rate = LEARNING_RATE
        self.__discount_rate = DISCOUNT_RATE

    def add_new_decisions_history(self, history: list[Decision]):
        self.__decisions = history.copy()

    def learn_using_history(self, was_destination_reached: bool):
        self.update_strategy_for_final_choice(self.__decisions[-1], was_destination_reached)
        for i in range(len(self.__decisions) - 2, -1, -1):
            decision = self.__decisions[i]
            next_decision = self.__decisions[i + 1]
            decision_rating = self.calculate_decision_rating(decision, next_decision)
            self.update_strategy(decision, decision_rating)

    def calculate_decision_rating(self, decision: Decision, next_decision: Decision):
        new = self.new_value_part(next_decision)
        old = self.old_value_part(decision)
        return new + old

    def update_strategy_for_final_choice(self, decision: Decision, was_destination_reached: bool):
        if (index := self.index(decision)) is None:
            self.__strategy.append(decision)
            index = len(self.__strategy) - 1
        value = DESTINATION_FIELD_PRICE if was_destination_reached else EMPTY_FIELD_COST
        self.__strategy[index].rating += value

    def new_value_part(self, next_decision: Decision):
        return self.__learning_rate * (EMPTY_FIELD_COST + (self.__discount_rate * self.get_strategy(next_decision.environment).rating))

    def old_value_part(self, decision: Decision):
        return (1 - self.__learning_rate) * self.get_decision(decision).rating

    def get_decision(self, decision: Decision) -> Decision:
        dec = list(filter(lambda d: d.environment == decision.environment and d.direction == decision.direction,
                          self.__strategy))
        return dec.pop() if len(dec) > 0 else Decision(decision.environment, decision.direction)

    def update_strategy(self, decision: Decision, rating: float):
        index = self.index(decision)
        if index is None:
            self.__strategy.append(decision)
            index = len(self.__strategy) - 1
        self.__strategy[index].rating = rating

    def get_distance(self, x1: int, y1: int, x2: int, y2: int):
        return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def index(self, decision: Decision):
        for i, dec in enumerate(self.__strategy):
            if dec.environment == decision.environment and dec.direction == decision.direction:
                return i
        return None

    def get_strategy(self, environment: list):
        decisions_list = self.get_environmental_decisions(environment)
        if len(decisions_list) > 0:
            return self.get_the_best_decision(decisions_list)
        return None

    def get_environmental_decisions(self, environment: list):
        return list(filter(lambda d: d.environment == environment, self.__strategy))

    def get_the_best_decision(self, decisions_list: list[Decision]):
        best_decision_rating = decisions_list[0].rating
        best_decision_index = 0
        for i, decision in enumerate(decisions_list):
            if decision.rating > best_decision_rating:
                best_decision_index = i
                best_decision_rating = decision.rating
        return decisions_list[best_decision_index]

    def __str__(self):
        message = ""
        for decision in self.__strategy:
            message += "[" + str(decision.environment) + " " + str(decision.direction) + " " + str(
                decision.rating) + "]\n"
        return message
