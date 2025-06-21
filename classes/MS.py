from classes.Pagina import Pagina

class MS:
    def __init__(self):
        self.processos = {}

    def alocarProcesso(self, processo):
        self.processos[processo.idProcesso] = processo

    def acessarPagina(self, IdProcesso, IdPagina):
        processo = self.processos.get(IdProcesso)
        if not processo:
            return None
        try:
            pagina_dados = processo.conteudoInicialResidente[IdPagina]
            pagina = Pagina(IdProcesso, IdPagina)
            pagina.conteudoPag = pagina_dados['conteudoPag']  # desserializa
            return pagina
        except IndexError:
            return None
        
    def atualizarPagina(self, pagina):
        processo = self.processos.get(pagina.idProcesso)
        if not processo:
            return

        if pagina.idPagina < len(processo.conteudoInicialResidente):
            processo.conteudoInicialResidente[pagina.idPagina] = self.serializarPagina(pagina)
        else:
            processo.conteudoInicialResidente.append(self.serializarPagina(pagina))

    def serializarPagina(self, pagina):
        return {
            'conteudoPag': pagina.conteudoPag
        }
