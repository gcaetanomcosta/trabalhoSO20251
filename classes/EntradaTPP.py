class EntradaTPP:
    def __init__(self, idProcesso, nPaginas):
        self.idProcesso = idProcesso
        self.nPaginas = nPaginas
    
    def getIdProcesso(self):
        return self.idProcesso
    
    def getNPaginas(self):
        return self.nPaginas
