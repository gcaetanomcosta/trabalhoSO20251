from .transformarEmBytes import transformarEmBytes
from .Quadro import Quadro
from .Pagina import Pagina
import math

class MPUsuario:

    def __init__(self, tamMPUsuario, tamPag, politicaSubstituicao):
        tamMPUsuario = transformarEmBytes(tamMPUsuario)
        tamPag = transformarEmBytes(tamPag)
        self.nQuadros = math.floor(tamMPUsuario/tamPag)
        self.quadrosMP = {}
        self.politicaSubstituicao = politicaSubstituicao
        self.tamPag = tamPag
        self.tamMPUsuario = tamMPUsuario
        #para fazer substituição por LRU, será usada como uma fila
        self.ultimosQuadrosReferenciados = []

        for i in range(self.nQuadros):
            self.quadrosMP[i*tamPag] = Quadro(i*tamPag, None)
    
    def adicionarUQR(self, end):
        if end in self.ultimosQuadrosReferenciados:
            self.ultimosQuadrosReferenciados.remove(end)
        self.ultimosQuadrosReferenciados.append(end)

    def removerUQR(self, end):
        self.ultimosQuadrosReferenciados.remove(end)

    def swapOutLRU(self, paginaNova, tabelasPaginas):
        quadroLRU = self.quadrosMP[self.ultimosQuadrosReferenciados[0]]
        #encontrando a tabela de pagina do quadro LRU
        tabelaPaginaLRU = tabelasPaginas[quadroLRU.getConteudoQuadro().getIdProcesso()]
        #verifica se a pagina foi modificada
        if tabelaPaginaLRU.verificarM(quadroLRU.getConteudoQuadro().getIdPagina()):
            #atualiazando valores na MS
            #MS.atualizarPagina(self.quadrosMP[self.ultimosQuadrosReferenciados[i]].getConteudoQuadro())
            print(f"Pagina {quadroLRU.getConteudoQuadro().getIdPagina()} do processo {quadroLRU.getConteudoQuadro().getIdProcesso()} atualizado na Memória Secundária ")
            self.quadrosMP[self.ultimosQuadrosReferenciados[0]].alocarPagina(paginaNova)
            #atualizando UQR
            self.adicionarUQR(quadroLRU.getEnd())
            #retornando o id do processo e da pagina que foi removida para atualizar a tabela de paginas no gerenciador de memoria
            #retornando também o endereço do quadro alocado para atualizar na tabela de paginas no gerenciador de memoria
            return [quadroLRU.getConteudoQuadro().getIdProcesso(), quadroLRU.getConteudoQuadro().getIdPagina()], quadroLRU.getEnd()
        
        #caso nao tenha sido modificada
        else:
            self.quadrosMP[self.ultimosQuadrosReferenciados[0]].alocarPagina(paginaNova)
            #atualizando UQR
            self.adicionarUQR(quadroLRU.getEnd())
            #retornando o id do processo e da pagina que foi removida para atualizar a tabela de paginas no gerenciador de memoria
            #retornando também o endereço do quadro alocado para atualizar na tabela de paginas no gerenciador de memoria
            return [quadroLRU.getConteudoQuadro().getIdProcesso(), quadroLRU.getConteudoQuadro().getIdPagina()], quadroLRU.getEnd()

    def swapOutRelogio(self, processo, tabelaPagina, nPaginasAlocadas, MS):
        """for i in range(processo.nPrePaginas()):    
            paginaNova = Pagina(i + nPaginasAlocadas, processo.getIdProcesso(), processo.paginar())
            #Selecionando pagina para ser suspensa
            
        
            #verifica se a pagina foi modificada
            if tabelaPagina.verificarM(nPaginasAlocadas + i):
                #atualizar valores na MS
                MS.atualizarPagina()"""
        pass

            

    def alocarPagina(self, pagina, tabelasPaginas):
        #Verificando disponibilidade de memória
        #Se houver memória disponivel, sera automaticamente alocado
        for i in range(self.nQuadros):
            #Caso o quadro i esteja disponivel
            if self.quadrosMP[i*self.tamPag].verificarDisponivel():
                #i serve como id da pagina, essencialmente é o número do quadro aqui.
                self.quadrosMP[i*self.tamPag].alocarPagina(pagina)
                #atualizando ultimosQuadrosReferenciados
                self.adicionarUltimosQuadrosReferenciados(i)
                return [], i*self.tamPag

        #caso não hajam quadros disponiveis:
        #LRU
        if self.politicaSubstituicao == "LRU":
            self.swapOutLRU(pagina, tabelasPaginas)

        #Relogio
        elif self.politicaSubstituicao == "Relógio":
            self.swapOutRelogio(pagina, tabelasPaginas)


    def desalocarPagina(self, end, tabelasPaginas):
        quadroComPagSaindo = self.quadrosMP[end]
        #encontrando a tabela de pagina do quadro LRU
        tabelaPaginaSaindo = tabelasPaginas[quadroComPagSaindo.getConteudoQuadro().getIdProcesso()]
        #verifica se a pagina foi modificada
        if tabelaPaginaSaindo.verificarM(quadroComPagSaindo.getConteudoQuadro().getIdPagina()):
            #atualiazando valores na MS
            #MS.atualizarPagina(self.quadrosMP[self.ultimosQuadrosReferenciados[i]].getConteudoQuadro())
            print(f"Pagina {quadroComPagSaindo.getConteudoQuadro().getIdPagina()} do processo {quadroComPagSaindo.getConteudoQuadro().getIdProcesso()} atualizado na Memória Secundária ")
            self.quadrosMP[end].limpar()
            #atualizando UQR
            self.removerUQR(quadroComPagSaindo.getEnd())
        #caso nao tenha sido modificada
        else:
            self.quadrosMP[self.ultimosQuadrosReferenciados[0]].limpar()
            #atualizando UQR
            self.removerUQR(quadroComPagSaindo.getEnd())
