class Processo:
    def __init__(self, idProcesso, conteudoInicialResidente, subProcessos = None):
        self.idProcesso = idProcesso
        self.conteudoInicialResidente = conteudoInicialResidente
        if subProcessos: self.subProcessos = subProcessos 
        else: self.subProcessos = []

    def getIdProcesso(self):
        return self.idProcesso
    
    def Paginar(self):
        return list(range(len(self.conteudoInicialResidente)))

    def nPrePaginas(self):
        return len(self.conteudoInicialResidente)
