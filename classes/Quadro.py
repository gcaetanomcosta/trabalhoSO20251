from .Pagina import Pagina

class Quadro:
    def __init__(self, end, conteudoQuadro):
        self.end = end
        self.conteudoQuadro = conteudoQuadro

    def limpar(self):
        self.conteudoQuadro = None

    def alocarPag(self, Pagina):
        self.conteudoQuadro = Pagina

    def verificarDisponivel(self):
        if self.conteudoQuadro == None: return True
        else: return False

    def getConteudoQuadro(self):
        return self.conteudoQuadro
    
    def getEnd(self):
        return self.end
