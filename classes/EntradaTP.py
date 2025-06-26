class EntradaTP:
    def __init__(self, bitP, bitM, endQuadroMP):
        self.bitP = bitP
        self.bitM = bitM
        self.endQuadroMP = endQuadroMP


    def getBitP(self):
        return self.bitP
    
    def getBitM(self):
        return self.bitM
    
    def getBitU(self):
        return self.bitU
    
    def getEndQuadroMP(self):
        return self.endQuadroMP
    
    def printarEntradaTP(self):
        print("bit P:", self.bitP, end=", ")
        print("bit M:", self.bitM, end=", ")
        print("Endereço Real:", self.endQuadroMP)

