class Processo:
    def __init__(self, idProcesso, conteudoInicialResidente, subProcessos = None):
        self.idProcesso = idProcesso
        self.conteudoInicialResidente = conteudoInicialResidente
        if subProcessos: self.subProcessos = subProcessos 
        else: self.subProcessos = []

    def getIdProcesso(self):
        return self.idProcesso
    
    def Paginar(self):
        lista = []
        for i in range(len(self.conteudoInicialResidente)):
            lista.append(i)
        return lista

    def nPrePaginas(self):
        return len(self.conteudoInicialResidente)
