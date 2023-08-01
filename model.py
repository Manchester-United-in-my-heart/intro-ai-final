import math
import random
import time

import numpy as np

class Cuckoo:
    def __init__(self, val, weight, capacity, N= 150, pa = 0.25, maxiter = 200 ):
        self.val = val
        self.weight = weight
        self.capacity = capacity
        self.N = N
        self.pa = pa
        self.maxiter = maxiter
        self.D = len(val)
        self.lb = [0] * self.D
        self.ub = [1] * self.D
        self.best_solution = []
        self.history = []
        self.beta = 1.5
        self.sigma = (math.gamma(1 + self.beta) * math.sin(math.pi * self.beta / 2) / (math.gamma((1 + self.beta) / 2) * self.beta * 2 ** ((self.beta - 1) / 2))) ** (1 / self.beta)
        self.population = None
        self.history.append(self.best_solution)
    def out(self, x):
        # calculate total weight
        total_weight = 0
        for i in range(len(x)):
            total_weight += x[i] * self.weight[i]
        if total_weight > self.capacity:
            return -1
        else:
            total_value = 0
            for i in range(len(x)):
                total_value += x[i] * self.val[i]
            return total_value
    def generate_initial_population(self):
        population = []
        for i in range(self.N):
            x = []
            for j in range(self.D):
                x.append(random.randint(0, 1))
            population.append(x)
        # create array contain ony 0's
        zero = [0] * self.D
        population[0] = zero
        return population
    def optimum(self, X, Y):
        if self.out(X) > self.out(Y):
            return X
        else:
            return Y
    def process(self):
        start = time.time()
        self.population = self.generate_initial_population()
        for iteration in range(self.maxiter):
            u = np.random.normal(0, self.sigma, self.D)
            v = np.random.normal(0, 1, self.D)
            S = u / abs(v) ** (1 / self.beta)

            # find current best solution
            for i in range(self.N):
                if i == 0:
                    self.best_solution = self.population[i]
                else:
                    self.best_solution = self.optimum(self.best_solution, self.population[i])

            # generate new generation
            new_population = self.population.copy()
            for i in range(self.N):
                if np.array_equal(self.population[i], self.best_solution):
                    continue
                new_population[i] += np.random.randn(self.D) * S * ( np.array(self.population[i]) - np.array(self.best_solution))
            # replace old generation
            for i in range(self.N):
                # pass the best solution
                if np.array_equal(self.population[i], self.best_solution):
                    continue
                # modify cuckoo nest with a probability pa
                if np.random.rand() < self.pa:
                    nest1, nest2 = random.sample(range(self.N), 2)
                    new_population[i] += np.random.rand() * (np.array(self.population[nest1]) - np.array(self.population[nest2]))
                # check bound
                for j in range(self.D):
                    if new_population[i][j] > 1:
                        new_population[i][j] = 1
                    elif new_population[i][j] < 0:
                        new_population[i][j] = 0
                    else:
                        new_population[i][j] = round(new_population[i][j])
                if self.out(new_population[i]) < self.out(self.population[i]):
                    new_population[i] = self.population[i]
            self.population = new_population
        best_solution = self.get_best_solution()
        best_value = self.out(best_solution)
        total_weight = self.get_weight()
        end = time.time()
        return  best_solution, best_value, total_weight, end - start
    def get_best_solution(self):
        for i in range(self.N):
            if i == 0:
                best_sol = self.population[i]
            else:
                best_sol = self.optimum(self.best_solution, self.population[i])
        best_sol = np.where(best_sol == 1, True, False)
        return best_sol
    def get_weight(self):
        best_solution = self.get_best_solution()
        total_weight = 0
        for i in range(len(best_solution)):
            if best_solution[i]:
                total_weight += self.weight[i]
        return total_weight

    def blind_search(self):
        start = time.time()
        best_value = -99999
        best_solution = []

        # branch and bound search
        def branch_and_bound(i, current_value, current_weight, current_solution):
            nonlocal best_value, best_solution
            if i == len(self.val):
                if current_value > best_value:
                    best_value = current_value
                    best_solution = current_solution
                return
            if current_weight + self.weight[i] <= self.capacity:
                branch_and_bound(i + 1, current_value + self.val[i], current_weight + self.weight[i], current_solution + [True])
            branch_and_bound(i + 1, current_value, current_weight, current_solution + [False])
        branch_and_bound(0, 0, 0, [])
        end = time.time()
        # get weight
        total_weight = 0
        for i in range(len(best_solution)):
            if best_solution[i]:
                total_weight += self.weight[i]
        return best_solution, best_value, total_weight, end - start