from pyparsing import List
from .EntradaTP import EntradaTP


##Retirar bit U daqui??????
class TabelaDePagina:
    def __init__(self, n_paginas: int):
        self.listaEntradasTP: List[EntradaTP] = [
            EntradaTP(bitP=0, bitM=0,
                    #    bitU=0, 
                       endQuadroMP=None)
            for _ in range(n_paginas)
        ]


    def adicionarEntrada(self, entrada: EntradaTP):
        self.listaEntradasTP.append(entrada)
    
    def ataulizarEnd(self, idPagina, end, bitP, bitM):
        if 0 <= idPagina < len(self.listaEntradasTP):
            entrada = self.listaEntradasTP[idPagina]
            entrada.endQuadroMP = end
            entrada.bitP = bitP
            entrada.bitM = bitM
        else:
            print(f"Página {idPagina} fora do intervalo.")

    def verificarM(self, idPagina):
        return self.listaEntradasTP[idPagina].bitM
    
    def get_entrada(self, idPagina: int) -> EntradaTP:
        return self.listaEntradasTP[idPagina]

    def set_bitU(self, idPagina: int, valor: int):
        self.listaEntradasTP[idPagina].bitU = valor
        
