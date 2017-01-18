import itertools
import random


class RandomMock:
    def __init__(self, numbers, seed = 0):
        ''' a number generator'''
        self.it = itertools.cycle(numbers)
        self.it_max = max(numbers)
        self.it_min = min(numbers)
        self.native_random = random.Random(seed)

    def randint(self, a, b):
        next_random = next(self.it)
        return a + (next_random) % (b - a)

    def randrange(self, stop):
        next_random = next(self.it)
        return next_random % stop

    def random(self):
        # use the max to obtain random fraction
        return self.native_random.random()

    def uniform(self, a, b):
        next_random = next(self.it)
        fraction = next_random /  (self.it_max - self.it_min)
        return a + (b - a) * fraction
