import copy
from statistics import mode
from chromosome import Chromosome
from individual import Individual
from utils import Utils
from random import randint, random, choices



class GeneticAlgorithm:
    def __init__(self,
                 population_length: int,
                 generations_num: int,
                 bits_num: int,
                 crossover_rate: float,
                 mutation_rate: float
                 ) -> None:
        """ GA Settings. """
        self.population: list[Individual] = []
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
            # Initialize the population by mutating the input sequences (adding random gaps).
            seqs_aux = [Utils.add_random_gaps(seq.copy()) for seq in sequences]
            # Create the individual.
            aux_pop.append(
                Individual(
                    [Chromosome(seq) for seq in seqs_aux],
                )
            )

        # Set the new population after a sanitization.
        self.population = list(map(Utils.sanitize_individual, aux_pop))

    def fitness(self) -> None:
        individuals_num = len(self.population)
        for ind_i in range(individuals_num):
            chromosomes_num = len(self.population[ind_i].chromosomes)
            # Represent the chromosomes one above the other (like a matrix).
            # [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
            chromosomes_matrix = [
                self.population[ind_i].chromosomes[chrom_i].genes for chrom_i in range(chromosomes_num)]
            cols_score = []
            for col in Utils.transpose_matrix(chromosomes_matrix):
                if mode(col) == '-' and ((len(col) - col.count('-')) <= 1):
                    continue

                # Calculate the column score.
                col_length = len(col)
                cols_score.append(col.count(mode(col)) // col_length)

            # Calculate the final score by adding the score of every column and, then,
            # multiply by 100 to represent the score as percentage.
            self.population[ind_i].score = (
                sum(cols_score) / len(chromosomes_matrix[0])) * 100

    # Roulette wheel selection.
    # TODO: research more about it.
    def selection(self) -> Individual:
        # Computes the totallity of the population fitness.
        population_fitness = sum(
            individual.score for individual in self.population)

        # Computes for each chromosome the probability.
        individual_probabilities = [
            individual.score/population_fitness for individual in self.population]

        return choices(self.population, weights=individual_probabilities, k=1)[0]

    def crossover(self, p1: Individual, p2: Individual) -> list[Individual]:
        # Children are copies of parents by default.
        c1, c2 = copy.copy(p1), copy.copy(p2)

        # Select random cut point.
        cut_point = randint(0, len(c1.chromosomes[0].genes)-1)

        # Represent the childs as a matrix to cut them given the cut point.
        c1_matrix = [list(chrom.genes) for chrom in c1.chromosomes]
        c2_matrix = [list(chrom.genes) for chrom in c2.chromosomes]

        # Cut the matrix.
        c1_matrix = [Utils.split_sequence(
            chrom, cut_point) for chrom in c1_matrix]
        c2_matrix = [Utils.split_sequence(
            chrom, cut_point) for chrom in c2_matrix]

        # Transpose matrix in order to crossover the matrix easily.
        c1_matrix = Utils.transpose_matrix(c1_matrix)
        c2_matrix = Utils.transpose_matrix(c2_matrix)

        # Crossover them.
        crossovered_c1 = [c1_matrix[0]] + [c2_matrix[1]]
        crossovered_c2 = [c2_matrix[0]] + [c1_matrix[1]]

        # Transpose again to get the crossovered matrix with the cols as rows and the rows as cols.
        c1_matrix = Utils.transpose_matrix(crossovered_c1)
        c2_matrix = Utils.transpose_matrix(crossovered_c2)

        # Update the childs.
        c1.chromosomes = [Chromosome(genes[0] + genes[1])
                          for genes in list(c1_matrix)]
        c2.chromosomes = [Chromosome(genes[0] + genes[1])
                          for genes in list(c2_matrix)]

        return [
            Utils.sanitize_individual(c1),
            Utils.sanitize_individual(c2)
        ]

    def mutation(self, individual: Individual) -> Individual:
        for chromosome in individual.chromosomes:
            for gen_i in range(len(chromosome.genes)):
                # Check for a mutation.
                if random() < self.mutation_rate:
                    # Put a gap.
                    chromosome.genes[gen_i] = '-'

        return individual

    def run(self, *files_path: str) -> Chromosome:
        # Initial population.
        self.initial_population(*files_path)

        # Keep track of the best solution.
        self.best = self.population[0]

        # Fitness function.
        self.fitness()

        for _ in range(self.generatons_num):
            # Check for new best solution.
            for i in range(self.generatons_num):
                if self.population[i].score > self.best.score:
                    self.best = self.population[i]

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

            # Replace population.
            self.population = children

        return self.best
