from .transformarEmBytes import transformarEmBytes
from .Quadro import Quadro
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
        
        # for i in range(self.nQuadros):
        #     self.quadrosMP[i*tamPag] = Quadro(i*tamPag, None)

        self.ponteiro_relogio = 0
        self.bit_uso = {}

        for i in range(self.nQuadros):
            endereco = i * tamPag
            self.quadrosMP[endereco] = Quadro(endereco, None)
            self.bit_uso[endereco] = 0
    
    def adicionarUQR(self, end):
        if end in self.ultimosQuadrosReferenciados:
            self.ultimosQuadrosReferenciados.remove(end)
        self.ultimosQuadrosReferenciados.append(end)
        self.bit_uso[end] = 1  # Marca o bit de uso

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

    def setBitU(self, endReal):
        self.bit_uso[endReal] = 1

    def swapOutRelogio(self, paginaNova, tabelasPaginas):
        while True:
            end_atual = list(self.quadrosMP.keys())[self.ponteiro_relogio]
            quadro = self.quadrosMP[end_atual]
            
            if self.bit_uso[end_atual] == 0:

                pagina_substituida = quadro.getConteudoQuadro()
                pid = pagina_substituida.getIdProcesso()
                id_pag = pagina_substituida.getIdPagina()

                if tabelasPaginas[pid].verificarM(id_pag):
                    print(f"Pagina {id_pag} do processo {pid} foi modificada. Salvando na MS.")
                    # self.MS.atualizarPagina(pagina_substituida)
                
                quadro.alocarPagina(paginaNova)
                self.bit_uso[end_atual] = 1
                self.ponteiro_relogio = (self.ponteiro_relogio + 1) % self.nQuadros

                return [pid, id_pag], end_atual
            else:
                self.bit_uso[end_atual] = 0
                self.ponteiro_relogio = (self.ponteiro_relogio + 1) % self.nQuadros
                

    def alocarPagina(self, pagina, tabelasPaginas):
        #Verificando disponibilidade de memória
        #Se houver memória disponivel, sera automaticamente alocado
        for i in range(self.nQuadros):
            #Caso o quadro i esteja disponivel
            if self.quadrosMP[i*self.tamPag].verificarDisponivel():
                #i serve como id da pagina, essencialmente é o número do quadro aqui.
                self.quadrosMP[i*self.tamPag].alocarPagina(pagina)
                #atualizando ultimosQuadrosReferenciados
                # self.adicionarUltimosQuadrosReferenciados(i)
                self.adicionarUQR(i*self.tamPag)
                return [], i*self.tamPag

        #caso não hajam quadros disponiveis:
        #LRU
        if self.politicaSubstituicao == "LRU":
            return self.swapOutLRU(pagina, tabelasPaginas)

        #Relogio
        elif self.politicaSubstituicao == "Relógio":
            return self.swapOutRelogio(pagina, tabelasPaginas)


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

    def printarMPUsuario(self):
        print("Memória Principal dos processos do usuário:", end="\n\n")
        indices = list(self.quadrosMP.keys())
        quadros = list(self.quadrosMP.values())
        #printar a mpusuario toda
        #for i in range(len(indices)):
        #printar apenas linhas ocupadas
        for i in range(len(self.ultimosQuadrosReferenciados)):
            print(indices[i], end=" ")
            quadros[i].printarQuadro()
            print("--------------------------------------------------------------------------------")

