from .EntradaTLB import EntradaTLB
  
class TLB:
  def __init__(self, n_linhas):
    self.n_linhas = n_linhas
    self.linhas = []

  def acessarTLB(self, idPagina):
    for i, entrada in enumerate(self.linhas):
      if entrada.idPagina == idPagina and entrada.validade == 1:
        self.linhas.append(self.linhas.pop(i))
        return entrada.endQuadroMP
    return -1

  def atualizarTLB(self, novaEntrada):
    for i, entrada in enumerate(self.linhas):
      if entrada.idPagina == novaEntrada.idPagina:
        self.linhas.pop(i)
        break
    if len(self.linhas) >= self.n_linhas:
      self.linhas.pop(0)
    self.linhas.append(novaEntrada)
