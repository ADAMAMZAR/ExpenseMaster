from datetime import time


class Expense:

    def __init__(self, name, category, amount, time=None):
        self.name = name
        self.category = category
        self.amount = amount
        self.time = time

    def __repr__(self):
        return f"<Expense: {self.name}, {self.category}, RM{self.amount:.2f}>"