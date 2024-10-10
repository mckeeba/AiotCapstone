class Counter:
    counter_value = 0

    @classmethod
    def increment_counter(cls):
        cls.counter_value += 1
        return cls.counter_value

if __name__ == "__main__":
    counter_instance = Counter()
    result = counter_instance.increment_counter()
    print(result)  # This will output the value to stdout
