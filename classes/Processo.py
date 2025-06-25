from .transformarEmBytes import transformarEmBytes
import math

class Processo:
    
    def __init__(self, idProcesso, tamProcesso, tamPag):
        self.idProcesso = idProcesso
        tamProcesso = tamProcesso
        self.conteudo = [0]*math.ceil(tamProcesso/tamPag)
        self.tamProcesso = len(self.conteudo)*tamPag

    def getIdProcesso(self):
        return self.idProcesso
    
    def getConteudo(self):
        return self.conteudo
    
    def getNPaginas(self):
        return len(self.conteudo)
    
    def getTamProcesso(self):
        return self.tamProcesso