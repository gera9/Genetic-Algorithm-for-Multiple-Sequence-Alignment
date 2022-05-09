from chromosome import Chromosome
from random import random

from individual import Individual


class Utils:
    """ Helper to write the best solution in a .txt file. """
    @staticmethod
    def generate_file_output(individual: Individual) -> bool:
        data = ''.join(''.join(chromosome.genes) +
                       '\n' for chromosome in individual.chromosomes)
        try:
            with open("output.txt", "w") as f:
                f.write(data)
        except(Exception):
            return False

        return True

    """ Orchestrate a complete sanitization. """
    @staticmethod
    def sanitize_individual(individual: Individual) -> Individual:
        Utils.complete_with_gaps(individual)

        # TODO: check...
        # Utils.delete_full_gaps_col(individual)

        Utils.complete_with_gaps(individual)

        return individual

    """ Delete columns full with gaps. """
    @staticmethod
    def delete_full_gaps_col(chromosome: Chromosome) -> Chromosome:
        ...

        return chromosome

    """ Add gaps at the end to have the chromosomes with the same length. """
    @staticmethod
    def complete_with_gaps(individual: Individual) -> Individual:
        # Complete with gaps.
        for i in range(len(individual.chromosomes)):
            diff = Utils.calc_genes_num(
                individual.chromosomes) - len(individual.chromosomes[i].genes)
            for _ in range(diff):
                individual.chromosomes[i].genes += "-"

        return individual

    """ The initial population mutation. """
    @staticmethod
    def add_random_gaps(chromosome: list[str]) -> list[str]:
        for i in range(len(chromosome)):
            # Check for a mutation.
            if random() < 0.09:
                # Put a gap.
                chromosome[i] = '-'

        return chromosome

    """ Read the text files where the sequences are placed. """
    @staticmethod
    def open_sequences_files(*files_path: str) -> list[list[str]]:
        files = []
        for path in files_path:
            with open(path) as f:
                files.append(
                    list(f.read().replace('\n', '').replace(' ', ''))
                )

        return files

    """ Calc the maximum number of genes of the chromosomes. """
    @staticmethod
    def calc_genes_num(chromosomes: list[Chromosome]) -> int:
        m_aux = 0
        lengths = []

        for chromosome in chromosomes:
            length = len(chromosome.genes)
            lengths.append(length)

            if length >= m_aux:
                m_aux = length

        return m_aux

    """ Count the number of no-gaps character in the chromosome. """
    @staticmethod
    def count_sequence_char(sequence: list[str]) -> int:
        return sum(char != '-' for char in sequence)

    # TODO: refact needed.
    """ Splite the chromosome to crossover later. """
    @staticmethod
    def split_sequence(sequence: list[str], limit: int) -> list[list[str]]:
        no_gaps_num, gaps_num = 0, 0
        for i in range(len(sequence)):
            if sequence[i] != '-' and no_gaps_num < limit:
                no_gaps_num += 1
            if sequence[i] == '-' and no_gaps_num < limit:
                gaps_num += 1
            if no_gaps_num == limit:
                break

        pt = (no_gaps_num + gaps_num)

        return [sequence[:pt], sequence[pt:]]

    """ Basic Lineal Algebra:  transpose a matrix to get the cols as rows and the rows as cols. """
    @staticmethod
    def transpose_matrix(matrix: list[list[str]]) -> list[list[str]]:
        rows_len = len(matrix)
        cols_len = len(matrix[0])

        return [[matrix[row_i][col_i] for row_i in range(rows_len)] for col_i in range(cols_len)]
