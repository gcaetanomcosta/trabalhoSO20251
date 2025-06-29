from .EntradaTP import EntradaTP

class TabelaDePagina:
    def __init__(self, n_paginas):
        self.listaEntradasTP = {}
        self.estadoProcesso = "pronto"
        for i in range(n_paginas):
            self.listaEntradasTP[i] = EntradaTP(bitP=0, bitM=0, endQuadroMP=None)
    

    def atualizarEntrada(self, idPagina, end, bitP, bitM):        
        self.listaEntradasTP[idPagina].endQuadroMP = end
        self.listaEntradasTP[idPagina].bitP = bitP
        self.listaEntradasTP[idPagina].bitM = bitM

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
            self.listaEntradasTP[i].bitP = 0
            self.listaEntradasTP[i].bitM = 0
            self.listaEntradasTP[i].endQuadroMP = None
        self.estadoProcesso = "bloqueado"

    def printarTP(self):
        print(f"Estado: {self.estadoProcesso}")
        print("Tabela de páginas:")
        entradas = list(self.listaEntradasTP.values())
        for i in range(len(entradas)):
            print(i, end=" ")
            entradas[i].printarEntradaTP()
            print("--------------------------------------------------------------------------------")