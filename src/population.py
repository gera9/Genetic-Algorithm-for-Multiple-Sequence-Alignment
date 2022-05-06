from chromosome import Chromosome


class Population:
    def __init__(self, chromosomes: list[Chromosome]) -> None:
        self.chromosomes = chromosomes
