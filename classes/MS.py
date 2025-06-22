import math
from .Pagina import Pagina
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
        return self.tamMS - totalOcupado 


    def alocarProcesso(self, processo):
        if processo.getTamProcesso() <= self.calcularDisponibilidade():
            self.processos[processo.idProcesso] = processo
        else:
            raise print("Não há espaço na memória secundária disponível para alocar o processo")
    
    def obterPaginaProcesso(self, idProcesso, idPagina):
        processo = self.processos[idProcesso]
        conteudo = processo.getConteudo()[idPagina]
        return Pagina(idProcesso, idPagina, conteudo)
    
