from classes.TabelaDePagina import TabelaDePagina


class EntradaTPP:
    def __init__(self, idProcesso, tp: TabelaDePagina, nPaginas):
        self.idProcesso = idProcesso
        self.tp = tp
        self.nPaginasa = nPaginas
