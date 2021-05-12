from agent.decision import Decision
from constants.constants import *


class StrategyBucket(object):

    def __init__(self):
        self.__decisions = []
        self.__learning_rate = LEARNING_RATE
        self.__discount_rate = DISCOUNT_RATE

    def add_strategy(self, strategy: list):
        strategy_length = len(strategy)
        for decision in strategy:
            decision.rating = self.calculate_decision_rating(decision, strategy_length)

    def calculate_decision_rating(self, decision, strategy_length):
        # TODO
        return 0

    def get_strategy(self, environment: list):
        for decision in self.__decisions:
            if decision.environment == environment:
                return decision
        return None

    def calculate_q_value(self, current_decision: Decision, new_decision: Decision):
        # todo
        pass

    def calculate_new_strategy(self, current_decision: Decision, new_decision: Decision):
        # TODO new improving strategy - calculate Q-Value
        self.__decisions.remove(current_decision)
        self.__decisions.append(new_decision)
