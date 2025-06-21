from Pagina import Pagina

class Quadro:
    def __init__(self, end, conteudoQuadro):
        self.end = end
        self.conteudoQuadro = conteudoQuadro

    def limpar(self):
        conteudoQuadro = None

    def alocarPag(self, Pagina):
        self.conteudoQuadro = Pagina

    def verificarDisponivel(self):
        if self.conteudoQuadro == None: return 1
        else: return 0
