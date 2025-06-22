class Pagina:
    def __init__(self, idProcesso, idPagina):
        self.idProcesso = idProcesso
        self.idPagina = idPagina
        self.conteudoPag = "conteudoIncial"

    # def escrever(self, conteudo):
    #     self.conteudoPag = conteudoPag

    def escrever(self):
        self.conteudoPag = "ConteudoModificado" 

    def ler(self):
        return self.conteudoPag
