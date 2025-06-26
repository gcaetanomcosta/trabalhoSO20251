class EntradaTLB:
    def __init__(self, validade, idPagina, bitP, bitM, endQuadroMP):
        self.validade = validade
        self.idPagina = idPagina
        self.bitP = bitP
        self.bitM = bitM
        self.endQuadroMP = endQuadroMP

    def getValidade(self):
        return self.validade
    
    def getIdPagina(self):
        return self.idPagina
    
    def getBitP(self):
        return self.bitP
    
    def getBitM(self):
        return self.bitM
    
    def getEndQuadroMP(self):
        return self.endQuadroMP
    
    def setValidade(self, valor):
        self.validade = valor

    def setIdPagina(self, valor):
        self.idPagina = valor

    def setBitP(self, valor):
        self.bitP = valor

    def setBitM(self, valor):
        self.bitM = valor

    def setEndQuadroMP(self, valor):
        self.endQuadroMP = valor    
    
    def printarEntradaTLB(self):
        print("Validade:", self.validade, end=", ")
        print("Página:", self.idPagina, end=", ")
        print("bit P:", self.bitP, end=", ")
        print("bit M:", self.bitM, end=", ")
        print("Endereço Real:", self.endQuadroMP)