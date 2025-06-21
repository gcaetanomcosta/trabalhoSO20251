class Processo:
    def __init__(self, idProcesso, conteudoInicialResidente, subProcessos = None):
        self.idProcesso = idProcesso
        self.conteudoInicialResidente = conteudoInicialResidente
        if subProcessos: self.subProcessos = subProcessos 
        else: self.subProcessos = []

    def Paginar(self):
        pass

    def nPrePaginas(self):
        return len(self.conteudoInicialResidente)
