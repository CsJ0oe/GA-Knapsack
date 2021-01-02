import random

class GeneticAlgorithm:
    def __init__(self, data, **kargs):
        self.data = data
        self.POPULATION_SIZE = kargs.get("population_size", 50)
        self.population = self._genPopulation()
        self.MAX_WEIGHT = kargs.get("max_weight", 12210)
        self.MAX_VOLUME = kargs.get("max_volume", 12)
        self.MAX_GENERATIONS =kargs.get("max_generations", 50)
        self.TOURNAMENT_SELECTION_SIZE = 5
        self.CROSSING_RATE = 0.8
        self.MUTATION_RATE = 0.2
    
    def fittest(self):
        return self.population[0]

    def printFittest(self):
        fittestOne = self.fittest()
        nb_items = [i for i in fittestOne if i == 1].__len__()
        print("\nselected {} items..".format(nb_items))

        for (i,(selected, item)) in enumerate(zip(self.fittest(), self.data)):
            if selected:
                print("\titem {}: weight={} volume={} price={} name={}".format(i, item[0], item[1], item[2], item[3]))

    def _genChromosome(self):
        return [random.randint(0,1) for _ in self.data]

    def _genPopulation(self):
        return [self._genChromosome() for _ in range(self.POPULATION_SIZE)]
    
    def _fitness(self, chromosome):
        weight, volume, price = 0, 0, 0
        for (selected, item) in zip(chromosome, self.data):
            if selected:
                weight += item[0]
                volume += item[1]
                price += item[2]
        if weight > self.MAX_WEIGHT or volume > self.MAX_VOLUME:
            price = 0
        return price
    
    def select_tournament(self, population):
        tournament_pop = []
        i = 0
        while i < self.TOURNAMENT_SELECTION_SIZE :
            tournament_pop.append(population[random.randrange(0,self.POPULATION_SIZE)])
            i += 1
        tournament_pop.sort(key=lambda x: self._fitness(x), reverse=True)
        
        return tournament_pop[0]

    def crossover_chromosomes(self, parent1, parent2):
        if random.random() < self.CROSSING_RATE: 
            child1 = self._genChromosome()
            child2 = self._genChromosome()

            '''One Point Cross Over'''
            index = random.randrange(1, child1.__len__())
            child1 = parent1[:index] + parent2[index:]
            child2 = parent2[:index] + parent1[index:]

            print("\nMaking a cross")
            print("Parent1: ",parent1)
            print("Parent2: ",parent2)
            print("Child1 : ", child1)
            print("Child1 : ", child2)

            return child1, child2
        else:
            return parent1, parent2

    def mutate_chromosome(self, chromosome):
        if random.random() < self.MUTATION_RATE:
            print("\nMaking a mutation")
            print("From: ",chromosome)

            random_bit_position = random.randrange(0,chromosome.__len__())
            if chromosome[random_bit_position] == 0:
                chromosome[random_bit_position] = 1
            else:
                chromosome[random_bit_position] = 0

            print("To:   ",chromosome)
        
        return chromosome
            
    def run(self):
        i = 0
        while i < self.MAX_GENERATIONS :
            i += 1
            new_population = []
            

            print("\nCrossover and Mutation Trace:")
            while new_population.__len__() < self.POPULATION_SIZE:
                parent1 = self.select_tournament(self.population)
                parent2 = self.select_tournament(self.population)


                child1, child2 = self.crossover_chromosomes(parent1, parent2)


                self.mutate_chromosome(child1)
                self.mutate_chromosome(child2)


                new_population.append(child1)

                # make sure to not depass the population size if we keep the elite
                if new_population.__len__() < self.POPULATION_SIZE:
                    new_population.append(child2)

            new_population.sort(key=lambda x: self._fitness(x), reverse=True)
            self.population = new_population

if __name__ == "__main__":
    # setup data (weight, volume, price, name)
    data = [(821, 0.8, 118, 'A'), (1144, 1, 322, 'B'), (634, 0.7, 166, 'C'), (701, 0.9, 195, 'D'),
            (291, 0.9, 100, 'E'), (1702, 0.8, 142, 'F'), (1633, 0.7, 100, 'G'), (1086, 0.6, 145, 'H'),
            (124, 0.6, 100, 'J'), (718, 0.9, 208, 'K'), (976, 0.6, 100, 'L'), (1438, 0.7, 312, 'M'),
            (910, 1, 198, 'W'), (148, 0.7, 171, 'S'), (1636, 0.9, 117, 'V'), (237, 0.6, 100, 'N'),
            (771, 0.9, 329, 'Z'), (604, 0.6, 391, 'P'), (1078, 0.6, 100, 'QA'), (640, 0.8, 120, 'O'),
            (1510, 1, 188, 'RE'), (741, 0.6, 271, 'JSU'), (1358, 0.9, 334, 'GT'), (1682, 0.7, 153, 'FA'),
            (993, 0.7, 130, 'TT'), (99, 0.7, 100, 'MA'), (1068, 0.8, 154, 'SA'), (1669, 1, 289, 'KI')]

    ga = GeneticAlgorithm(data, max_weight=12210, max_volume=12, max_generations=50, population_size=200) 

    ga.run()     # run the GA
    print(ga.printFittest()) 