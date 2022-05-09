from chromosome import Chromosome

""" An Individual contains n chromosomes (in this case protein sequences). """


class Individual:
    def __init__(self, chromosomes: list[Chromosome]) -> None:
        self.chromosomes = chromosomes
        self.score: float = 0.0

    def __str__(self) -> str:
        return ''.join(chromosome.__str__() for chromosome in self.chromosomes)
