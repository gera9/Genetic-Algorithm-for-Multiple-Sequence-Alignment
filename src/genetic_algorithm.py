import copy
from statistics import mode
from chromosome import Chromosome
from utils import Utils
from numpy import array, random
from numpy.random import rand


class GeneticAlgorithm:
    def __init__(self,
                 population_length: int,
                 generations_num: int,
                 bits_num: int,
                 crossover_rate: float,
                 mutation_rate: float
                 ) -> None:
        """ GA Settings. """
        self.population: list[Chromosome] = []
        # Define the population size.
        self.population_length = population_length
        # Define the total of generations.
        self.generatons_num = generations_num
        # Bits number.
        self.bits_num = bits_num
        # Crossover rate.
        self.crossover_rate = crossover_rate
        # Mutation rate.
        self.mutation_rate = mutation_rate / float(bits_num)

        """ Best chromosome tracker. """
        self.best = None

    def initial_population(self, *files_path: str) -> None:
        sequences = Utils.open_sequences_files(*files_path)
        # TODO: delete it.
        #sequences = [list('ABCDEFGHIJ'), list('ABCDEFGHIJKLMN')]

        aux_pop = []
        for _ in range(self.population_length):
            seqs_aux = []
            for seq in sequences:
                seqs_aux.append(
                    Utils.add_random_gaps(seq.copy())
                )
            aux_pop.append(
                Chromosome(
                    seqs_aux
                )
            )

        self.population = list(map(Utils.sanitize_chromosome, aux_pop))

    # TODO: refactor needed.
    def fitness(self) -> None:
        for i in range(len(self.population)):
            scores = []
            # Traverse by columns.
            for col in array(self.population[i].genes).T:
                col_length = len(col)
                gaps_num = col_length - Utils.count_sequence_char(col)
                if (col_length - gaps_num) > 1:
                    # Calculate the score
                    n = list(col).count(mode(col))
                    if n > 1:
                        score = list(col).count(mode(col)) / col_length
                        scores.append(score)

            self.population[i].score = (
                sum(scores)/len(self.population[i].genes[0]))*100

    # Roulette wheel selection.
    # TODO: research more about it.
    def selection(self) -> Chromosome:
        # Computes the totallity of the population fitness.
        population_fitness = sum(
            [chromosome.score for chromosome in self.population])

        # Computes for each chromosome the probability.
        chromosome_probabilities = [
            chromosome.score/population_fitness for chromosome in self.population]

        return random.choice(self.population, p=chromosome_probabilities)

    # TODO: refactor needed.
    def crossover(self, p1: Chromosome, p2: Chromosome) -> list[Chromosome]:
        # Children are copies of parents by default.
        c1, c2 = copy.copy(p1), copy.copy(p2)

        middle_point = Utils.count_sequence_char(c1.genes[0]) // 2

        # Check for recombination.
        if rand() < self.crossover_rate:
            aux_c1, aux_c2 = [], []
            for i in range(len(c1.genes)):
                aux_c1.append(Utils.split_sequence(c1.genes[i], middle_point)[
                    0] + Utils.split_sequence(c2.genes[i], middle_point)[1])

            for i in range(len(c2.genes)):
                aux_c2.append(Utils.split_sequence(c2.genes[i], middle_point)[
                    0] + Utils.split_sequence(c1.genes[i], middle_point)[1])

            for i in range(len(aux_c1)):
                c1.genes[i] = aux_c1[i]

            for i in range(len(aux_c2)):
                c2.genes[i] = aux_c2[i]

        c1 = Utils.sanitize_chromosome(c1)
        c2 = Utils.sanitize_chromosome(c2)

        return [c1, c2]

    def mutation(self, chromosome: Chromosome) -> None:
        for gene in chromosome.genes:
            for i in range(len(gene)):
                # Check for a mutation.
                if rand() < self.mutation_rate:
                    # Put a gap.
                    gene[i] == '-'

        return chromosome

    def run(self, *files_path: str) -> Chromosome:
        # Initial population.
        self.initial_population(*files_path)

        # Keep track of best solution.
        self.best = self.population[0]

        # Fitness function.
        self.fitness()

        for gen in range(self.generatons_num):
            # Check for new best solution.
            for i in range(self.generatons_num):
                if self.population[i].score > self.best.score:
                    self.best = self.population[i]
                    print('--- Best founded at generation {} ---'.format(gen))
                    print(self.best)

            # Selection.
            selected = [self.selection()
                        for _ in range(self.population_length)]

            # Next generation.
            children = []
            for i in range(0, self.population_length, 2):
                # Get selected parents in pairs.
                p1, p2 = selected[i], selected[i+1]

                # Crossover.
                for chromosome in self.crossover(p1, p2):
                    # Mutation.
                    self.mutation(chromosome)
                    # Store for next generation
                    children.append(chromosome)

            # Replace population
            self.population = children

        return self.best
