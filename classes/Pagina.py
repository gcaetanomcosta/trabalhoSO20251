class Pagina:
    def __init__(self, idProcesso, idPagina, conteudo):
        self.idProcesso = idProcesso
        self.idPagina = idPagina
        self.conteudoPag = conteudo

    def escrever(self, conteudoNovo):
        self.conteudoPag = conteudoNovo

    def ler(self):
        return self.conteudoPag
    
    def getIdPagina(self):
        return self.idPagina
    
    def getIdProcesso(self):
        return self.idProcesso
