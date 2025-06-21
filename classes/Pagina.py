class Pagina:
    def __init__(self, idProcesso, idPagina, conteudoPag):
        self.idProcesso = idProcesso
        self.idPagina = idProcesso
        self.conteudoPag = conteudoPag

    def escrever(self, conteudo):
        self.conteudoPag = conteudoPag

    def ler(self):
        return self.conteudoPag
