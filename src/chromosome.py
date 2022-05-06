class Chromosome:
    def __init__(self, genes: list[list[str]]) -> None:
        self.genes = genes
        self.score = 0.0

    def __str__(self) -> str:
        template = ''
        for i in range(len(self.genes)):
            template += '[{}]\n'.format(', '.join([str(gene)
                                        for gene in self.genes[i]]))
        return template
