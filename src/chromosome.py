class Chromosome:
    def __init__(self, genes: list[str]) -> None:
        self.genes = genes

    def __str__(self) -> str:
        return '[{}]\n'.format(', '.join(self.genes))
