from chromosome import Chromosome
from numpy.random import rand
from numpy import array


class Utils:
    """ Helper to write the best solution in a .txt file. """
    @staticmethod
    def generate_file_output(chromosome: Chromosome) -> bool:
        data = ''
        for gene in chromosome.genes:
            data += '{}\n'.format(''.join(gene))
        with open("output.txt", "w") as f:
            f.write(data)
        return True

    """ Orchestrate a complete sanitization. """
    @staticmethod
    def sanitize_chromosome(chromosome: Chromosome) -> Chromosome:
        Utils.complete_with_gaps(chromosome)

        # TODO: check...
        # Utils.delete_full_gaps_col(chromosome)

        Utils.complete_with_gaps(chromosome)

        return chromosome

    """ Delete columns full with gaps. """
    @staticmethod
    def delete_full_gaps_col(chromosome: Chromosome) -> Chromosome:
        cols = array(chromosome.genes).T
        cols_num = len(cols)
        rows_num = len(cols[0])

        elements_to_delete = []
        for i in range(cols_num):
            if list(cols[i]).count('-') == rows_num:
                elements_to_delete.append(i)

        for i in range(len(chromosome.genes)):
            for e in elements_to_delete:
                chromosome.genes[i].remove(chromosome.genes[i][e])

        return chromosome

    """ Add gaps at the end to have the chromosomes with the same length. """
    @staticmethod
    def complete_with_gaps(chromosome: Chromosome) -> Chromosome:
        # Complete with gaps.
        for i in range(len(chromosome.genes)):
            diff = Utils.calc_genes_num(
                chromosome.genes) - len(chromosome.genes[i])
            for j in range(diff):
                chromosome.genes[i] += "-"

        return chromosome

    """ The initial population mutation. """
    @staticmethod
    def add_random_gaps(chromosome: list[str]) -> list[str]:
        for i in range(len(chromosome)):
            # Check for a mutation.
            if rand() < 0.09:
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
    def calc_genes_num(chromosomes: list[list[str]]) -> int:
        m_aux = 0
        lengths = []

        for chromosome in chromosomes:
            length = len(chromosome)
            lengths.append(length)

            if length >= m_aux:
                m_aux = length

        return m_aux

    """ Count the number of no-gaps character in the chromosome. """
    @staticmethod
    def count_sequence_char(sequence: list[str]) -> int:
        count = 0
        for char in sequence:
            if char != '-':
                count += 1
        return count

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
