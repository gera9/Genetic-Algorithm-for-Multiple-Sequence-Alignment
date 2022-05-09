from individual import Individual

""" A Population contains n Individuals (in this case the multiple sequences). """


class Population:
    def __init__(self, individuals: list[Individual]) -> None:
        self.individuals = individuals
