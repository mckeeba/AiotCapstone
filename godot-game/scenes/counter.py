class Counter:
    def __init__(self):
        self.counter_value = 0

    def increment(self):
        self.counter_value += 1
        return self.counter_value
