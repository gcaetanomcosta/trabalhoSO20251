from EntradaTPP import EntradaTPP
from Processo import Processo

class TabelaPagProcesso:
    def __init__(self):
        self.lista_entradas = []

    def adicionarEntrada(self, entrada):
        self.lista_entradas.append(entrada)
    
    def novoProcesso(self, Processo):
        entrada = EntradaTPP(processo.idProcesso, processo.nPrePaginas())
        adicionarEntrada(entrada)
        print("Processo {processo.idProcesso} adicionado à tabela")

    def excluirProcesso(self, idProcesso):
        antes = len(self.lista_entradas)
        nova_lista = []
        for e in self.lista_entradas:
            if e.idProcesso != idProcesso:
                nova_lista.append(e)
        self.lista_entradas = nova_lista
        if antes == len(self.lista_entradas):
            print("Processo {idProcesso} não encontrado")
        else:
            print("Processo {idProcesso} removido da tabela")
