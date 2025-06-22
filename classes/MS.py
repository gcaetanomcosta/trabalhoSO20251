import math
from .transformarEmBytes import transformarEmBytes

class MS:
    def __init__(self, tamMS):
        self.processos = {}
        self.tamMS = transformarEmBytes(tamMS)

    def calcularDisponibilidade(self):
        totalOcupado = 0
        processos = self.processos.values()
        for processo in processos:
            totalOcupado += processo.getTamProcesso()
        return totalOcupado 


    def alocarProcesso(self, processo):
        if processo.getTamProcesso() <= self.calcularDisponibilidade():
            self.processos[processo.idProcesso] = processo
        else:
            raise print("Não há memória na memória secundária disponível para alocar o processo")
    
    def obterPaginaProcesso(self, idProcesso, idPagina, tamCR):
        processo = self.processos[idProcesso]
        nConjuntosR = math.ceil(processo.getNPaginas()/tamCR)
        conjuntoResidenteNovo = tamCR//idPagina
        conteudo = processo.getConteudo()[conjuntoResidenteNovo*tamCR:(conjuntoResidenteNovo*tamCR+tamCR)]
        return conteudo
    
