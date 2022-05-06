from genetic_algorithm import GeneticAlgorithm
from utils import Utils
import time


def main() -> None:
    # Initialize Genetic Algorithm object.
    ga = GeneticAlgorithm(
        bits_num=21,
        population_length=20,
        generations_num=20,
        crossover_rate=0.9,
        mutation_rate=1.0
    )

    start = time.time()

    # Run it.
    best = ga.run(
        './src/sequences/Omicron.txt',
        './src/sequences/Alpha.txt',
        './src/sequences/Bat.txt',
        './src/sequences/Beta.txt'
    )

    end = time.time()

    if Utils.generate_file_output(best):
        total_time = (end - start)
        print('--- Done! ---')
        print('--- Execution time: {0:.2f} s ---'.format(total_time))
        print('--- Score solution: {} % ---'.format(best.score))


if __name__ == '__main__':
    main()
