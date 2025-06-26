from .EntradaTLB import EntradaTLB
  
class TLB:
    def __init__(self, n_linhas):
        self.n_linhas = int(n_linhas)
        self.linhasOcupadas = 0
        #para realocar linhas da propria TLB
        self.cabecote = 0
        self.linhas = []
        for i in range(self.n_linhas):
           self.linhas.append(EntradaTLB(0, 0, 0, 0, 0))

    def reiniciarTLB(self):
        self.linhasOcupadas = 0
        self.cabecote = 0
        for i in range(self.n_linhas):
           self.linhas[i].setValidade(0)
        print("TLB reiniciada com sucesso!")

    def adicionarPagTLB(self, validade, idPagina, bitP, bitM, endQuadroMP):
        if self.linhasOcupadas < self.n_linhas:
            self.linhas[self.cabecote] = EntradaTLB(validade, idPagina, bitP, bitM, endQuadroMP)
            self.linhasOcupadas += 1
            self.cabecote += 1
            if self.cabecote >= self.n_linhas:
                self.cabecote = 0
        else:
            self.linhas[self.cabecote] = EntradaTLB(validade, idPagina, bitP, bitM, endQuadroMP)
            self.cabecote += 1
            if self.cabecote >= self.n_linhas:
                self.cabecote = 0
        print(f"Página {idPagina} adicionada à TLB")

    def atualizarPagTLB(self, validade, idPagina, bitP, bitM, endQuadroMP):
        for i in range(self.n_linhas): 
            if self.linhas[i].getIdPagina() == idPagina:
                self.linhas[i] = EntradaTLB(validade, idPagina, bitP, bitM, endQuadroMP)
        raise print(f"Página {idPagina} não está na TLB, logo não pode ser atualizada")

    def verificarPresencaPag(self, idPagina):
        for i in range(self.n_linhas):
            if self.linhas[i].getIdPagina() == idPagina and self.linhas[i].getValidade() == 1:
                return True
        return False
    
    def printarTLB(self):
        print("Linhas da TLB:")
        for i in range(len(self.linhas)):
            print(i, end=" ")
            self.linhas[i].printarEntradaTLB()
            print("--------------------------------------------------------------------------------")