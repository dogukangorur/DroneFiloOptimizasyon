# ga_optimizer.py

import random
from a_star_solver import a_star_search

class GAOptimizer:
    def __init__(self, drones, deliveries, nfzs, nodes_map, adj_list, pop_size=10, generations=20, mutation_rate=0.1):
        self.drones = drones
        self.deliveries = deliveries
        self.nfzs = nfzs
        self.nodes_map = nodes_map
        self.adj_list = adj_list
        self.pop_size = pop_size
        self.generations = generations
        self.mutation_rate = mutation_rate

    def create_individual(self):
        return {delivery.point_id: random.choice(self.drones).drone_id for delivery in self.deliveries}

    def create_population(self):
        return [self.create_individual() for _ in range(self.pop_size)]

    def fitness(self, individual):
        score = 0
        for delivery_id, drone_id in individual.items():
            drone = next(d for d in self.drones if d.drone_id == drone_id)
            delivery = next(dp for dp in self.deliveries if dp.point_id == delivery_id)

            if drone.max_weight < delivery.weight:
                score -= 100
                continue

            start_node = f"D{drone_id}_START"
            goal_node = str(delivery_id)
            path, cost = a_star_search(self.adj_list, self.nodes_map, self.nfzs, start_node, goal_node)
            if not path:
                score -= 100
                continue

            score += delivery.priority * 10
            score -= cost * 0.2

        return score

    def selection(self, population):
        return sorted(population, key=lambda x: self.fitness(x), reverse=True)[:2]

    def crossover(self, parent1, parent2):
        child = {}
        for key in parent1.keys():
            child[key] = parent1[key] if random.random() > 0.5 else parent2[key]
        return child

    def mutate(self, individual):
        for key in individual.keys():
            if random.random() < self.mutation_rate:
                individual[key] = random.choice(self.drones).drone_id
        return individual

    def run(self):
        population = self.create_population()
        for generation in range(self.generations):
            selected = self.selection(population)
            new_population = selected[:]
            while len(new_population) < self.pop_size:
                child = self.crossover(*selected)
                child = self.mutate(child)
                new_population.append(child)
            population = new_population

        best = max(population, key=lambda x: self.fitness(x))
        return best
