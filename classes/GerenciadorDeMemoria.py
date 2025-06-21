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
        self.MPUsuario = MPUsuario(self.configuracoesSistema["tamMPUsuario"], self.configuracoesSistema["tamPag"])
        self.TLB = TLB(self.configuracoesSistema["nLinhasTLB"])
        self.MS = MS(self.configuracoesSistema["tamMS"])

    def mapearEndReal(self, endL):
        pass

    def admissao(self, pagina):
        pass

    def liberar(self, pagina):
        pass

    def despar(self, pagina):
        pass

    def pausar(self, pagina):
        pass

    def desbloquear(self, pagina):
        pass

    def suspender(self, pagina):
        pass

    def realizarInstrucao(self, instrucao):
        pass
    
    def operarInterface(self):
        pass

    