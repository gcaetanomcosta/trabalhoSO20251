from .transformarEmBytes import transformarEmBytes
from .Quadro import Quadro
from .Pagina import Pagina

class MPUsuario:

    def __init__(self, tamMPUsuario, tamPag, politicaSubstituicao):
        tamMPUsuario = transformarEmBytes(tamMPUsuario)
        tamPag = transformarEmBytes(tamPag)
        self.nQuadros = int(tamMPUsuario/tamPag)
        self.quadrosMP = []
        self.politicaSubstituicao = politicaSubstituicao
        #para fazer substituição por LRU, será usada como uma fila
        self.ultimosQuadrosReferenciados = []

        for i in range(self.nQuadros):
            self.quadrosMP.append(Quadro(i*tamPag*8, Pagina(i, [])))
    
    def adicionarUQR(self, idQuadro):
        if idQuadro in self.ultimosQuadrosReferenciados:
            self.ultimosQuadrosReferenciados.remove(idQuadro)
        self.ultimosQuadrosReferenciados.append(idQuadro)

    def swapOutLRU(self, processo, tabelaPagina, nPaginasAlocadas, MS):
        for i in range(processo.nPrePaginas()):
            paginaNova = Pagina(i + nPaginasAlocadas, processo.getIdProcesso(), processo.paginar())
            #verifica se a pagina foi modificada
            if tabelaPagina.verificarM(nPaginasAlocadas + i):
                #atualiazando valores na MS
                MS.atualizarPagina(self.quadrosMP[self.ultimosQuadrosReferenciados[i]].getConteudoQuadro())
                self.quadrosMP[self.ultimosQuadrosReferenciados[i]].alocarPagina(paginaNova)
            #caso nao tenha sido modificada
            else:
                self.quadrosMP[self.ultimosQuadrosReferenciados[i]].alocarPagina(paginaNova)


    def swapOutRelogio(self, processo, tabelaPagina, nPaginasAlocadas, MS):
        for i in range(processo.nPrePaginas()):    
            paginaNova = Pagina(i + nPaginasAlocadas, processo.getIdProcesso(), processo.paginar())
            #Selecionando pagina para ser suspensa
            
        
            #verifica se a pagina foi modificada
            if tabelaPagina.verificarM(nPaginasAlocadas + i):
                #atualizar valores na MS
                MS.atualizarPagina()

            

    def alocarProcesso(self, processo, tabelaPagina, MS):
        #Verificando disponibilidade de memória
        #Se houver memória disponivel, sera automaticamente alocado, sem levar em conta localidade temporal ou espacial
        idProcesso = processo.getIdProcesso()
        nPaginasAlocadas = 0
        for i in range(self.nQuadros):
            #Caso o quadro i esteja disponivel
            if self.quadrosMP[i].verificarDisponivel():
                #i serve como id da pagina, essencialmente é o número do quadro aqui.
                self.quadrosMP[i].alocarPagina(Pagina(i, idProcesso, processo.paginar()))
                nPaginasAlocadas += 1
                #salvando em ultimosQuadrosReferenciados
                self.adicionarUltimosQuadrosReferenciados(i)

        #caso não hajam quadros disponiveis mas o processo ainda possui conteudo para ser paginado residentemente:
        if processo.nPrePaginas() > 0:

            #LRU
            if self.politicaSubstituicao == "LRU":
                self.swapOutLRU(processo, tabelaPagina, nPaginasAlocadas, MS)

            #Relogio
            elif self.politicaSubstituicao == "Relógio":
                self.swapOutRelogio(processo, tabelaPagina, nPaginasAlocadas, MS)

        


















































"""

from .transformarEmBits import transformarEmBits
from .Quadro import Quadro
from .Pagina import Pagina

class MPUsuario:

    def __init__(self, tamMPUsuario, tamPag, nLinhasTLB, politicaSubstituicao):
        tamMPUsuario = transformarEmBits(tamMPUsuario)
        tamPag = transformarEmBits(tamPag)
        self.nQuadros = int(tamMPUsuario/tamPag)
        self.quadrosMP = []

        self.politicaSubstituicao = politicaSubstituicao

        #para fazer localidade espacial e temporal. Usando tamanho maximo para ultimos quadros referenciados arbitrariamente como tamanho da TLB, que representa justamente o número máximo de páginas que um processo único pode ter.
        #para quadros referenciados antes do máximo de uma TLB serão considerados como não tendo sido utilizados recentemente e logo não serão poupados pelo swap out.
        self.tamMaxUQR = nLinhasTLB
        self.ultimosQuadrosReferenciados = []

        for i in range(self.nQuadros):
            self.quadrosMP.append(Quadro(i*tamPag*8, Pagina(i, [])))
    
    def adicionarUltimosQuadrosReferenciados(self, idQuadro):
        if len(self.ultimosQuadrosReferenciados) == self.tamMaxUQR:
            
        else:


    def alocarProcesso(self, processo):
        #Verificando disponibilidade de memória
        #Se houver memória disponivel, sera automaticamente alocado, sem levar em conta localidade temporal ou espacial
        idProcesso = processo.getIdProcesso()
        algumaPaginaAlocada = False
        while processo.nPrePaginas() != 0:
            #Se nenhuma pagina for alocada em uma iteração é porque a MP do Usuario está sem memória disponivel
            nPaginasAlocadas = 0
            for i in range(self.nQuadros):
                #Caso o quadro i esteja disponivel
                if self.quadrosMP[i].verificarDisponivel():
                    #i serve como id da pagina, essencialmente é o número do quadro aqui.
                    self.quadrosMP[i].alocarPagina(Pagina(i, idProcesso, processo.paginar()))
                    nPaginasAlocadas += 1
                    #salvando em ultimosQuadrosReferenciados para acabar com o risco de paginas do proprio processo sofrerem swapout
                    self.ultimosQuadrosReferenciados.adicionarUltimosQuadrosReferenciados(i)
            #se chegar ao fim do loop e nPaginasAlocadas for zero passar pra alocação no caso de não haver quadros disponiveis
            if nPaginasAlocadas == 0:
                break
            else: 
                algumaPaginaAlocada = True

        #caso não hajam quadros disponiveis
        for i in range():
            #Seguindo principio da localidade espacial e temporal para fazer swap
            #Escolher o quadro mais distante do ultimo referenciado que n tenha sido utilizado recentemente
            #Fazendo isso usando ultimosQuadrosRefenciados
            #Idealmente as paginas de um processo precisam ser alocadas proximas. 
            #Se tiver quadro com acesso recente precisa pular na hora de alocar o processo. Estou utilizando o tamanho máximo de um processo como recente em relação a lista de ultimos quadros referenciados. 
            #iteração de busca por swap out será feita em duas direções a partir de um ponto inicial até achar um quadro ideal para swap out pelo principio de localidade espacial e temporal.
            
            #Determinando aonde começar a buscar por quadro ideal para swap out
            #Começando a busca por swap out pelo quadro mais distante do ultimo referenciado caso nenhuma pagina do processo tenha sido alocada
            if not algumaPaginaAlocada:
                #determinar o quadro mais distante do ultimo referenciado
                primeiroQuadroIterSwapOut = self.ultimosQuadrosReferenciados[-1] - int(self.nQuadros/2)
                if primeiroQuadroIterSwapOut < 0:
                    primeiroQuadroIterSwapOut = self.nQuadros + primeiroQuadroIterSwapOut
            #Caso alguma pagina tenha sido alocada começar a busca por swap out a partir desse ponto. Paginas do proprio processo serão ignoradas pelo swap out por conta do principio da localidade
            if algumaPaginaAlocada:
                primeiroQuadroIterSwapOut = self.ultimosQuadrosReferenciados[-1]
            
            #Loop de busca por swap out
            for i in range(0, len):

                #iteração pelos quadros antes do selecionado como inicio
                if primeiroQuadroIterSwapOut - i >= 0:
                    
                else:
                    self.nQuadros - primeiroQuadroIterSwapOut - i



                #iteração pelos quadros depois do selecionado como fim
                if primeiroQuadroIterSwapOut + i < self.nQuadros:

                else:


"""