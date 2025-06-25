import math
import sys
from .EntradaTPP import EntradaTPP
from .ListaDeInstrucoes import ListaDeInstrucoes
from .TabelaDePagina import TabelaDePagina
from .TabelaPagProcesso import TabelaPagProcesso
from .transformarEmBytes import transformarEmBytes
from .MPUsuario import MPUsuario
from .MS import MS
from .TLB import TLB
from .Processo import Processo


class GerenciadorDeMemoria:
    
    def __init__(self, argv):
        #Usuario se quiser customizar as configurações do sistema precisa por 5 argumentos na hora de chamar o main, além do próprio main.py.
        #O tamanho da TLB precisa ser proporcional ao tamanho do endL e ao tamanho da pagina. o endereço lógico guarda o offset dentro de uma pagina e a referencia da pagina dentro de um processo, o numero de linhas da TLB precisa ser do tamanho maximo do conjunto residente de um processo, justamente o endereço logico menos os bits do offset.
        #Se o usuario colocar algo que não faça sentido por enquanto o programa irá crachar em algum momento. Perguntar para professora se pode deixar assim no dia da entrega final. Se não, criar um tratamento de entradas.
        if len(argv) == 6:
            self.configuracoesSistema = {"tamMPUsuario": argv[1], "tamPag": argv[2], "tamEndL": argv[3], "nLinhasTLB": argv[4], "tamMS": argv[5], "politicaSubstituicao": argv[6]}
        else:
            self.configuracoesSistema = {"tamMPUsuario": "4GB", "tamPag": "16MB", "tamEndL": "32bits", "nLinhasTLB": "64", "tamMS": "256GB", "politicaSubstituicao": "LRU"}
            #self.configuracoesSistema = {"tamMPUsuario": "4GB", "tamPag": "2MB", "tamEndL": "32bits", "nLinhasTLB": "64", "tamMS": "256GB", "politicaSubstituicao": "LRU"}

        self.tabelasPaginas = {}
        self.processoExecutando = None
        self.TabelaPagProcesso = TabelaPagProcesso()
        self.filaBloqueado = []
        self.filaPronto = []
        self.MPUsuario = MPUsuario(self.configuracoesSistema["tamMPUsuario"], self.configuracoesSistema["tamPag"], self.configuracoesSistema["politicaSubstituicao"])
        self.TLB = TLB(self.configuracoesSistema["nLinhasTLB"])
        self.MS = MS(self.configuracoesSistema["tamMS"])

    def mapearEndReal(self, pid, endL):
        tamPag = transformarEmBytes(self.configuracoesSistema["tamPag"])
        # tamEndL = self.configuracoesSistema["tamEndL"]
        # if endL > int(self.configuracoesSistema["tamEndL"].split()[0]):
        #     raise print("Endereço lógico inserido é maior que o permitido no sistema")
        # else:
        #     return self.tabelasPaginas(pid)[endL//tamPag].getEndQuadroMP()

        tamEndL = int(self.configuracoesSistema["tamEndL"].replace("bits", "").strip())

        if endL >= 2 ** tamEndL: # Potencia de 2 adicionada para verificar o tamanho máximo do endereço lógico
            raise print("Endereço lógico excede o tamanho permitido")

        idPagina = endL // tamPag
        print(f"Endereço lógico {endL} corresponde à página {idPagina} e offset {endL % tamPag}")
        return self.tabelasPaginas[pid].getListaEntradasTP()[idPagina].endQuadroMP

        

    def admissao(self, pid: str, tamanho_bytes: int):

        tam_pagina = transformarEmBytes(self.configuracoesSistema["tamPag"])
        #num_paginas é tam_processo / tam_pagina arrendondado para cima 
        num_paginas = math.ceil(tamanho_bytes / tam_pagina)  # arredondamento para cima

        tabela_de_paginas = TabelaDePagina(num_paginas)
        self.tabelasPaginas[pid] = tabela_de_paginas

        self.TabelaPagProcesso.adicionarEntrada(EntradaTPP(pid, num_paginas))

        print(f"\n[{pid}] Processo criado com {tamanho_bytes} bytes e ({num_paginas} páginas).")
        print(f"[{pid}] Tabela de Páginas inicializada:\n")


        processo = Processo(pid, tamanho_bytes, tam_pagina)
        self.MS.alocarProcesso(processo)

        # Se alguma pagina foi removida da MP para adicionar essa, precisa atualizar na respectiva tabela de pagina
        paginaRemovida, endQuadroAlocado = self.MPUsuario.alocarPagina(self.MS.obterPaginaProcesso(pid, 0), self.tabelasPaginas)
        #pagina removida é [idProcesso, idPagina]
        if paginaRemovida != []:
            self.tabelasPaginas[paginaRemovida[0]].atualizarEntrada(paginaRemovida[1], None, 0, 0, 0)
            if self.tabelasPaginas[paginaRemovida[0]].getEstadoProcesso() == "pronto":
                self.tabelasPaginas[paginaRemovida[0]].setEstadoProcesso("pronto suspenso")
            elif self.tabelasPaginas[paginaRemovida[0]].getEstadoProcesso() == "bloqueado":
                self.tabelasPaginas[paginaRemovida[0]].setEstadoProcesso("bloqueado suspenso")
            
        #atualizando a tabela de pagina do processo novo para incluir a presença da primeira pagina em MP
        self.tabelasPaginas[pid].atualizarEntrada(0, endQuadroAlocado, 1, 0, 0)

        for id_pagina, entrada in tabela_de_paginas.listaEntradasTP.items():
            print(f"  Página {id_pagina:02d} -> P: {entrada.bitP}, M: {entrada.bitM}, Quadro: {entrada.endQuadroMP}")

        #Adicionando na fila de pronto
        self.filaPronto.append(pid)
        print(f"Processo {pid} adicionado na fila dos prontos")


        print(f"\n[{pid}] TPP atualizada com sucesso.\n")
        print(f"Admissão do processo {pid} finalizada com sucesso")

    def liberar(self, pid):
        enderecosComPagDoProcesso = []
        tabelaPaginaProcessoSaindo = self.tabelasPaginas[pid]
        #obtendo lista de endereços dos quadros que possuem paginas do processo a ser desalocado
        for entrada in list(tabelaPaginaProcessoSaindo.getListaEntradasTP().values()):
            enderecosComPagDoProcesso.append(entrada.getEndQuadroMP())
        #desalocando cada pagina do processo
        for end in enderecosComPagDoProcesso:
            self.MPUsuario.desalocarPagina(end, self.tabelasPaginas)
        #limpando TLB
        if self.processoExecutando == pid:
            self.TLB.reiniciarTLB()
            print(f"TLB reiniciada")
        #Removendo das tabelas
        self.tabelasPaginas.pop(pid)
        print(f"Tabela de paginas do processo {pid} removida")
        self.TabelaPagProcesso.pop(pid)
        print(f"Processo {pid} removido da tabela de paginas por processo")
        #Removendo das filas
        if pid in self.filaBloqueado:
            self.filaBloqueado.remove(pid)
            print(f"Processo {pid} removido da fila dos bloqueados")
        if pid in self.filaPronto:
            self.filaPronto.remove(pid)
            print(f"Processo {pid} removido da fila dos prontos")
        
        
        print(f"Liberação do processo {pid} finalizada com sucesso")
        

    def bloquear(self, pid):
        if "suspenso" in self.tabelasPaginas[pid].getEstadoProcesso(): 
            self.tabelasPaginas[pid].setEstadoProcesso("bloqueado suspenso")
        else:
            self.tabelasPaginas[pid].setEstadoProcesso("bloqueado")
        if pid in self.filaPronto:
            self.filaPronto.remove(pid)
            print(f"Processo {pid} removido da fila dos prontos")
        if pid not in self.filaBloqueado:
            self.filaBloqueado.append(pid)
            print(f"Processo {pid} adicionado na fila dos bloqueados")
        print(f"Bloqueio do processo {pid} finalizado com sucesso")

    def ler(self, pid, endLogico):
        tamPag = transformarEmBytes(self.configuracoesSistema["tamPag"])
        #atualizando estado executando e pronto
        if self.processoExecutando != pid:
            if self.processoExecutando is not None:
                # Se o processo que estava executando não é o pid, ele volta para pronto
                self.tabelasPaginas[self.processoExecutando].setEstadoProcesso("pronto")
            self.tabelasPaginas[pid].setEstadoProcesso("executando")
            self.TLB.reiniciarTLB()

        #pagina está na memória
        endReal = self.mapearEndReal(pid, endLogico) 
        if endReal != None:
            #fazer logica do bit u aqui.
            self.MPUsuario.adicionarUQR(endReal)
            print(f"Conteudo do endereço lógico {endLogico} do processo {pid} no endereço real {endReal} lido com sucesso!")
            #verificar se página está na TLB
            if not self.TLB.verificarPresencaPag(endLogico//tamPag):
                #adicionando página na TLB
                self.TLB.adicionarPagTLB(1, endLogico//tamPag, 1, self.tabelasPaginas[pid][endLogico//tamPag].getBitM(), endReal)
        #pagina não está na memória
        else:
            tamPag = transformarEmBytes(self.configuracoesSistema["tamPag"])
            print(f"Falta de página! Iniciando procedimento de alocação da página {endLogico//tamPag} do processo {pid}")
            # Se alguma pagina foi removida da MP para adicionar essa, precisa atualizar na respectiva tabela de pagina    
            paginaRemovida, endQuadroAlocado = self.MPUsuario.alocarPagina(self.MS.obterPaginaProcesso(pid, endLogico//tamPag), self.tabelasPaginas)
            #pagina removida é [idProcesso, idPagina]
            if paginaRemovida != []:
                self.tabelasPaginas[paginaRemovida[0]].atualizarEntrada(paginaRemovida[1], None, 0, 0, 0)
                if self.tabelasPaginas[paginaRemovida[0]].getEstadoProcesso() == "pronto":
                    self.tabelasPaginas[paginaRemovida[0]].setEstadoProcesso("pronto suspenso")
                elif self.tabelasPaginas[paginaRemovida[0]].getEstadoProcesso() == "bloqueado":
                    self.tabelasPaginas[paginaRemovida[0]].setEstadoProcesso("bloqueado suspenso")

            #atualizando TLB se a pagina removida estiver na TLB
            if paginaRemovida[0] == self.processoExecutando:
                self.TLB.atualizarPagTLB(1, paginaRemovida[1], 0, 0, 0)

            #atualizando a tabela de pagina do processo novo para incluir a presença da primeira pagina em MP
            self.tabelasPaginas[pid].atualizarEntrada(0, endQuadroAlocado, 1, 0, 0)

            for i, entrada in enumerate(self.tabelasPaginas[pid].listaEntradasTP):
                print(f"  Página {i:02d} -> P: {entrada.bitP}, M: {entrada.bitM}, Quadro: {entrada.endQuadroMP}")
            print(f"Tabela de paginas do processo {pid} atualizada")
            self.ler(pid, endLogico)


    def escrever(self, pid, endLogico):
        #atualizando estado executando e pronto
        if self.processoExecutando != pid:
            if self.processoExecutando is not None:
                # Se o processo que estava executando não é o pid, ele volta para pronto
                self.tabelasPaginas[self.processoExecutando].setEstadoProcesso("pronto")
            self.tabelasPaginas[pid].setEstadoProcesso("executando")
            self.TLB.reiniciarTLB()

        #pagina está na memória
        tamPag = transformarEmBytes(self.configuracoesSistema["tamPag"])
        endReal = self.mapearEndReal(pid, endLogico) 
        if endReal != None:
            #fazer logica do bit u aqui.
            self.MPUsuario.adicionarUQR(endReal)
            self.tabelasPaginas[pid].setBitM(endLogico//tamPag, 1)
            print(f"Operação de escrita no endereço lógico {endLogico} do processo {pid} no endereço real {endReal} finalizado com sucesso!")
            #verificar se página está na TLB
            if not self.TLB.verificarPresencaPag(endLogico//tamPag):
                #adicionando página na TLB
                self.TLB.adicionarPagTLB(1, endLogico//tamPag, 1, self.tabelasPaginas[pid][endLogico//tamPag].getBitM(), endReal)
        #pagina não está na memória
        else:
            print(f"Falta de página! Iniciando procedimento de alocação da página {endLogico//tamPag} do processo {pid}")
            # Se alguma pagina foi removida da MP para adicionar essa, precisa atualizar na respectiva tabela de pagina    
            paginaRemovida, endQuadroAlocado = self.MPUsuario.alocarPagina(self.MS.obterPaginaProcesso(pid, endLogico//tamPag), self.tabelasPaginas)
            #pagina removida é [idProcesso, idPagina]
            if paginaRemovida != []:
                self.tabelasPaginas[paginaRemovida[0]].atualizarEntrada(paginaRemovida[1], None, 0, 0, 0)
                if self.tabelasPaginas[paginaRemovida[0]].getEstadoProcesso() == "pronto":
                    self.tabelasPaginas[paginaRemovida[0]].setEstadoProcesso("pronto suspenso")
                elif self.tabelasPaginas[paginaRemovida[0]].getEstadoProcesso() == "bloqueado":
                    self.tabelasPaginas[paginaRemovida[0]].setEstadoProcesso("bloqueado suspenso")
            #atualizando TLB se a pagina removida estiver na TLB
            if paginaRemovida[0] == self.processoExecutando:
                self.TLB.atualizarPagTLB(1, paginaRemovida[1], 0, 0, 0)

            #atualizando a tabela de pagina do processo novo para incluir a presença da primeira pagina em MP
            self.tabelasPaginas[pid].atualizarEntrada(0, endQuadroAlocado, 1, 0, 0)

            for i, entrada in enumerate(self.tabelasPaginas[pid].listaEntradasTP):
                print(f"  Página {i:02d} -> P: {entrada.bitP}, M: {entrada.bitM}, Quadro: {entrada.endQuadroMP}")
            print(f"Tabela de paginas do processo {pid} atualizada")
            self.escrever(pid, endLogico)

    def instrucaoCPU(self, pid, endLogico):
        tamPag = transformarEmBytes(self.configuracoesSistema["tamPag"])
        #atualizando estado executando e pronto
        if self.processoExecutando != pid:
            if self.processoExecutando is not None:
                self.tabelasPaginas[self.processoExecutando].setEstadoProcesso("pronto")
            self.tabelasPaginas[pid].setEstadoProcesso("executando")
            self.TLB.reiniciarTLB()
    
        #pagina está na memória
        endReal = self.mapearEndReal(pid, endLogico) 
        if endReal != None:
            #fazer logica do bit u aqui.
            self.MPUsuario.adicionarUQR(endReal)
            print(f"Instrução localizada no endereço lógico {endLogico} do processo {pid} no endereço real {endReal} realizada com sucesso!")
            #verificar se página está na TLB
            if not self.TLB.verificarPresencaPag(endLogico//tamPag):
                #adicionando página na TLB
                self.TLB.adicionarPagTLB(1, endLogico//tamPag, 1, self.tabelasPaginas[pid][endLogico//tamPag].getBitM(), endReal)
        #pagina não está na memória
        else:
            tamPag = transformarEmBytes(self.configuracoesSistema["tamPag"])
            print(f"Falta de página! Iniciando procedimento de alocação da página {endLogico//tamPag} do processo {pid}")
            # Se alguma pagina foi removida da MP para adicionar essa, precisa atualizar na respectiva tabela de pagina    
            paginaRemovida, endQuadroAlocado = self.MPUsuario.alocarPagina(self.MS.obterPaginaProcesso(pid, endLogico//tamPag), self.tabelasPaginas)
            #pagina removida é [idProcesso, idPagina]
            if paginaRemovida != []:
                self.tabelasPaginas[paginaRemovida[0]].atualizarEntrada(paginaRemovida[1], None, 0, 0, 0)

            #atualizando TLB se a pagina removida estiver na TLB
            if paginaRemovida[0] == self.processoExecutando:
                self.TLB.atualizarPagTLB(1, paginaRemovida[1], 0, 0, 0)

            #atualizando a tabela de pagina do processo novo para incluir a presença da primeira pagina em MP
            self.tabelasPaginas[pid].atualizarEntrada(0, endQuadroAlocado, 1, 0, 0)

            for i, entrada in enumerate(self.tabelasPaginas[pid].listaEntradasTP):
                print(f"  Página {i:02d} -> P: {entrada.bitP}, M: {entrada.bitM}, Quadro: {entrada.endQuadroMP}")
            print(f"Tabela de paginas do processo {pid} atualizada")
            self.instrucaoCPU(pid, endLogico)

    def realizarInstrucao(self, instrucao):
        tipo = instrucao.tipo
        pid = instrucao.pid

        match tipo:
            case "C":
                tamanho = instrucao.get_tamanho_em_bytes()
                print(f"[{pid}] Criar processo com {tamanho} bytes")
                self.admissao(pid, tamanho)

            case "R":
                endereco = instrucao.get_endereco_logico()
                print(f"[{pid}] Leitura no endereço lógico {endereco}")
                self.ler(pid, endereco)

            case "W":
                endereco = instrucao.get_endereco_logico()
                print(f"[{pid}] Escrita no endereço lógico {endereco}")
                self.escrever(pid, endereco)

            case "P":
                endereco = instrucao.get_endereco_logico()
                print(f"[{pid}] Executar instrução no endereço lógico {endereco}")
                self.instrucaoCPU(pid, endereco)

            case "I":
                dispositivo = instrucao.args[0]
                print(f"[{pid}] Requisição de I/O no dispositivo '{dispositivo}'")
                self.bloquear(pid)

            case "T":
                print(f"[{pid}] Terminar processo")
                self.liberar(pid)

            case _:
                print(f"[{pid}] Instrução desconhecida: {instrucao}")
    
    def carregar_instrucoes(self, caminho: str) -> ListaDeInstrucoes:
        try:
            lista = ListaDeInstrucoes(caminho)
            print(f"\n[OK] Arquivo carregado com {len(lista)} instruções válidas.")

            print("\nInstruções válidas:")
            for i, instrucao in enumerate(lista, start=1):
                print(f"{i:02d}: {instrucao}")
            
            if lista.erros:
                print(f"[!] {len(lista.erros)} instruções ignoradas por erro de sintaxe:\n")
                for erro in lista.erros:
                    print(erro)
                    sys.exit(1)


            return lista

        except FileNotFoundError as e:
            print(f"Erro ao carregar o arquivo: {e}")
            sys.exit(1)

    def operarInterface(self):
        caminho = "classes/entradas/entrada1.txt"
        lista_instrucoes = self.carregar_instrucoes(caminho)
        for instrucao in lista_instrucoes:
            input(f"\nPressione Enter para executar a instrução: {instrucao}")
            print(f"\nExecutando: {instrucao}")
            self.realizarInstrucao(instrucao)
        pass

    