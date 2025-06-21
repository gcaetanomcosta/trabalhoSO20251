import sys
from classes.ListaDeInstrucoes import ListaDeInstrucoes
from .MPUsuario import MPUsuario
from .MS import MS
from .TLB import TLB

class GerenciadorDeMemoria:
    
    def __init__(self, argv):
        #Usuario se quiser customizar as configurações do sistema precisa por 5 argumentos na hora de chamar o main, além do próprio main.py.
        #O tamanho da TLB precisa ser proporcional ao tamanho do endL e ao tamanho da pagina. o endereço lógico guarda o offset dentro de uma pagina e a referencia da pagina dentro de um processo, o numero de linhas da TLB precisa ser do tamanho maximo do conjunto residente de um processo, justamente o endereço logico menos os bits do offset.
        #Se o usuario colocar algo que não faça sentido por enquanto o programa irá crachar em algum momento. Perguntar para professora se pode deixar assim no dia da entrega final. Se não, criar um tratamento de entradas.
        if len(argv) == 6:
            self.configuracoesSistema = {"tamMPUsuario": argv[1], "tamPag": argv[2], "tamEndL": argv[3], "nLinhasTLB": argv[4], "tamMS": argv[5], "politicaSubstituicao": argv[6]}
        else:
            self.configuracoesSistema = {"tamMPUsuario": "4GB", "tamPag": "16MB", "tamEndL": "32bits", "nLinhasTLB": "64", "tamMS": "256GB", "politicaSubstituicao": "LRU"}

        self.listaTabPag = []
        self.TabelaPagProcesso = []
        # self.MPUsuario = MPUsuario(self.configuracoesSistema["tamMPUsuario"], self.configuracoesSistema["tamPag"], self.configuracoesSistema["politicaSubstituicao"])
        # self.TLB = TLB(self.configuracoesSistema["nLinhasTLB"])
        # self.MS = MS(self.configuracoesSistema["tamMS"])

    def mapearEndReal(self, endL):
        pass

    def admissao(self, pagina):
        pass

    def liberar(self, pagina):
        pass

    def despachar(self, pagina):
        pass

    def pausar(self, pagina):
        pass

    def desbloquear(self, pagina):
        pass

    def suspender(self, pagina):
        pass

    def realizarInstrucao(self, instrucao):
        tipo = instrucao.tipo
        pid = instrucao.pid

        match tipo:
            case "C":
                tamanho = instrucao.get_tamanho_em_bytes()
                print(f"[{pid}] Criar processo com {tamanho} bytes")
                # TODO: chamar admissao()

            case "R":
                endereco = instrucao.get_endereco_logico()
                print(f"[{pid}] Leitura no endereço lógico {endereco}")
                # TODO: mapearEndReal(), consultar TLB, tratar falta de página

            case "W":
                endereco = instrucao.get_endereco_logico()
                valor = instrucao.get_valor()
                print(f"[{pid}] Escrita no endereço lógico {endereco} com valor {valor}")
                # TODO: mapearEndReal(), setar bit de modificação

            case "P":
                endereco = instrucao.get_endereco_logico()
                print(f"[{pid}] Executar instrução no endereço lógico {endereco}")
                # TODO: simular fetch da instrução (como um R)

            case "I":
                dispositivo = instrucao.args[0]
                print(f"[{pid}] Requisição de I/O no dispositivo '{dispositivo}'")
                # TODO: pausar o processo, simular operação de I/O

            case "T":
                print(f"[{pid}] Terminar processo")
                # TODO: liberar recursos, remover páginas

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
            print(f"Executando: {instrucao}")
            self.realizarInstrucao(instrucao)
        pass

    