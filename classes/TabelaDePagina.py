from .EntradaTP import EntradaTP

class TabelaDePagina:
    def __init__(self, n_paginas):
        self.listaEntradasTP = {}
        for i in range(n_paginas):
            self.listaEntradasTP[i] = EntradaTP(bitP=0, bitM=0, bitU=0, endQuadroMP=None)
    
    def atualizarEntrada(self, idPagina, end, bitP, bitM, bitU):
        entrada = self.listaEntradasTP[idPagina]
        entrada.endQuadroMP = end
        entrada.bitP = bitP
        entrada.bitM = bitM
        entrada.bitU = bitU

    def verificarM(self, idPagina):
        return self.listaEntradasTP[idPagina].getBitM()
    
    def verificarU(self, idPagina):
        return self.listaEntradasTP[idPagina].getBitU()
    
    def verificarP(self, idPagina):
        return self.listaEntradasTP[idPagina].getBitP()

    def setBitU(self, idPagina, valor):
        self.listaEntradasTP[idPagina].bitU = valor
    
    def setBitP(self, idPagina, valor):
        self.listaEntradasTP[idPagina].bitP = valor

    def setBitM(self, idPagina, valor):
        self.listaEntradasTP[idPagina].bitM = valor
        
