from .EntradaTPP import EntradaTPP
from .Processo import Processo

class TabelaPagProcesso:
    def __init__(self):
        self.lista_entradas = {}

    def adicionarEntrada(self, entrada : EntradaTPP):
        self.lista_entradas[entrada.getIdProcesso()] = entrada
    
    def novoProcesso(self, processo):
        entrada = EntradaTPP(processo.idProcesso, processo.nPrePaginas())
        self.adicionarEntrada(entrada)
        print(f"Processo {processo.idProcesso} adicionado à tabela de paginas por processo")

    def excluirProcesso(self, idProcesso):
        antes = len(self.lista_entradas)
        nova_lista = []
        for e in self.lista_entradas:
            if e.idProcesso != idProcesso:
                nova_lista.append(e)
        self.lista_entradas = nova_lista
        if antes == len(self.lista_entradas):
            raise print(f"Processo {idProcesso} não encontrado")
        else:
            print(f"Processo {idProcesso} removido da tabela de paginas por processo")
    
    def printarTPP(self):
        entradas = list(self.lista_entradas.values())
        print("Tabela de páginas por processo:")
        for i in range(len(entradas)):
            print(i, end=" ")
            entradas[i].printarEntradaTPP()
            print("--------------------------------------------------------------------------------")
