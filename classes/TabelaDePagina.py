class TabelaDePagina:
    def __init__(self):
        self.listaEntradasTP = []

    def adicionarEntrada(self, entrada):
        self.listaEntradasTP.append(entrada)
    
    def ataulizarEnd(self, idPagina, end, bitP, bitM):
        if 0 <= idPagina < len(self.listaEntradasTP):
            entrada = self.listaEntradasTP[idPagina]
            entrada.endQuadroMP = end
            entrada.bitP = bitP
            entrada.bitM = bitM
        else:
            print(f"Página {idPagina} fora do intervalo.")

    def verificarM(self, idPagina):
        return self.listaEntradasTP[idPagina].bitM
        
