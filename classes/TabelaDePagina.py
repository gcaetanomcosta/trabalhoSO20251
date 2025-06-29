from .EntradaTP import EntradaTP

class TabelaDePagina:
    def __init__(self, n_paginas):
        self.listaEntradasTP = {}
        self.estadoProcesso = "pronto"
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

    def setEstadoProcesso(self, valor):
        self.estadoProcesso = valor
        
    def getListaEntradasTP(self):
        return self.listaEntradasTP
    
    def getEstadoProcesso(self):
        return self.estadoProcesso
    
    def bloquearProcesso(self):
        for i in range(len(list(self.listaEntradasTP.values()))):
            self.listaEntradasTP[i].bitU = 0
            self.listaEntradasTP[i].bitP = 0
            self.listaEntradasTP[i].bitM = 0
            self.listaEntradasTP[i].endQuadroMP = None
        self.estadoProcesso = "bloqueado"

