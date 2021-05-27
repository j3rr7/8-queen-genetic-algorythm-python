import math
import random
import sys

random.seed(random.randrange(sys.maxsize))


class QUEEN:
    def __init__(self, arrays: list, fitness: int):
        self.arrays = arrays
        self.fitness = fitness


class GeneticAlgorythm:
    """
        Generate random list of 1D array and return
    """
    @staticmethod
    def generate_random_data(max_size: int = 1) -> list:
        return [[random.randrange(8) for _ in range(8)] for _ in range(max_size)]

    """
        Calculate fitness of single 1D array best fitness is 28 return is int
    """
    @staticmethod
    def calculate_fitness(array: list) -> int:
        BEST_FITNESS = 28

        horizontal_collisions = sum([array.count(queen) - 1 for queen in array]) / 2
        diagonal_collisions = 0

        n = len(array)
        left_diagonal = [0] * 2 * n
        right_diagonal = [0] * 2 * n

        for i in range(n):
            left_diagonal[i + array[i] - 1] += 1
            right_diagonal[len(array) - i + array[i] - 2] += 1

        diagonal_collisions = 0

        for i in range(2 * n - 1):
            counter = 0
            if left_diagonal[i] > 1:
                counter += left_diagonal[i] - 1
            if right_diagonal[i] > 1:
                counter += right_diagonal[i] - 1
            diagonal_collisions += counter / (n - abs(i - n + 1))

        return int(BEST_FITNESS - (horizontal_collisions + diagonal_collisions))

    """
        Return the best possible solution without displaying the history
    """
    @staticmethod
    def run_genetic_algorithm(arrays: list, _gen: int, _cros: float, _mut: float, inf: bool = False):
        if len(arrays) <= 1:
            return arrays

        if inf:
            _gen = float('inf')

        old_population = arrays.copy()
        new_population = []

        counter = 0
        while counter < _gen:
            old_population.sort(key=lambda x: x.fitness, reverse=True)
            if random.random() < _cros:
                parent1 = old_population[0].arrays
                parent2 = old_population[1].arrays
                children = GeneticAlgorythm.generate_children(parent1, parent2, False)
                [new_population.append(QUEEN(array, GeneticAlgorythm.calculate_fitness(array))) for array in children]
                if random.random() < _mut:
                    children = GeneticAlgorythm.mutate_children(children)
                    [new_population.append(QUEEN(array, GeneticAlgorythm.calculate_fitness(array))) for array in
                     children]
                if GeneticAlgorythm.calculate_fitness(children[0]) == 28 or GeneticAlgorythm.calculate_fitness(children[1]) == 28:
                    break
            else:
                new_population.append(old_population[0])
                new_population.append(old_population[1])
                #old_population = new_population
            counter += 1
        return new_population

    """
        return the child of 2 1D parent
    """
    @staticmethod
    def generate_children(parent1: list, parent2: list, rnd: bool = False) -> list:
        n = len(parent1)
        if rnd:
            c = random.randint(0, n - 1)
        else:
            c = 3
        return [(parent1[0:c] + parent2[c:n]), (parent2[0:c] + parent1[c:n])]

    """
        Mutate random integer inside 1D arrays
    """
    @staticmethod
    def mutate_children(arrays: list):
        return [GeneticAlgorythm.mutate(array) for array in arrays]

    """
        Mutate random integer inside 1D array
    """
    @staticmethod
    def mutate(x):
        n = len(x)
        #c = random.randint(0, n - 1)
        #m = random.randint(1, n)
        c = random.randrange(8)
        m = random.randrange(8)
        x[c] = m
        return x
