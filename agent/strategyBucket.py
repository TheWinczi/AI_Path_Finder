from agent.decision import Decision


class StrategyBucket(object):

    def __init__(self):
        self.__decisions = []

    def add_strategy(self, new_decision: Decision):
        current_decision = self.get_strategy(new_decision.environment)
        if current_decision is None:
            self.__decisions.append(new_decision)
        self.calculate_new_strategy(current_decision, new_decision)

    def get_strategy(self, environment: list):
        for decision in self.__decisions:
            if decision.environment == environment:
                return decision
        return None

    def calculate_new_strategy(self, current_decision: Decision, new_decision: Decision):
        # TODO new improving strategy
        self.__decisions.remove(current_decision)
        self.__decisions.append(new_decision)
