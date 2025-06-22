from typing import Optional


class EntradaTP:
    def __init__(self, bitP: int, bitM: int, 
                #  bitU: int, 
                 endQuadroMP: Optional[int]):
        self.bitP = bitP
        self.bitM = bitM
        # self.bitU = bitU
        self.endQuadroMP = endQuadroMP
