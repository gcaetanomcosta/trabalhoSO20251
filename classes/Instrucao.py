from .transformarEmBytes import transformarEmBytes


class Instrucao:
    TIPOS_VALIDOS = {"C", "P", "R", "W", "I", "T"}

    def __init__(self, pid: str, tipo: str, args: list[str]):
        self.pid = pid.upper()  # Ex: P1
        self.tipo = tipo.upper()  # Ex: C, R, W, etc
        self.args = args  # Lista de strings
        self.validar()

    def validar(self):
        if self.tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de instrução inválido: {self.tipo}")

        if self.tipo == "C" and len(self.args) != 2:
            raise ValueError("Instrução 'C' precisa de dois argumentos: tamanho e unidade")

        if self.tipo in {"R", "P", "w"} and len(self.args) != 1:
            raise ValueError(f"Instrução '{self.tipo}' precisa de 1 argumento (endereço lógico)")

        if self.tipo == "I" and len(self.args) != 1:
            raise ValueError("Instrução 'I' precisa de 1 argumento (dispositivo)")

        if self.tipo == "T" and self.args:
            raise ValueError("Instrução 'T' não deve ter argumentos")

    def get_endereco_logico(self) -> int | None:
        """Retorna o endereço lógico como inteiro se aplicável."""
        if self.tipo in {"R", "W", "P"}:
            return int(self.args[0].replace("(", "").replace(")10", ""))
        return None

    def get_tamanho_em_bytes(self) -> int | None:
        "Retorna o tamanho da imagem de processo (para instruções C)"
        if self.tipo == "C":
            try:
                valor_com_unidade = self.args[0] + self.args[1].upper()  # Ex: "500MB"
                return transformarEmBytes(valor_com_unidade)
            except Exception as e:
                raise ValueError(f"Instrução 'C' malformada. Esperado: <tamanho> <unidade>. Erro: {e}")
        return None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        tipo_descricao = {
            "C": "Criação",
            "P": "Execução",
            "R": "Leitura",
            "W": "Escrita",
            "I": "Entrada/Saída",
            "T": "Terminação"
        }

        descricao = tipo_descricao.get(self.tipo, "Desconhecida")
        argumentos = " ".join(map(str, self.args)) if self.args else ""
        return f"[{self.pid}] {descricao} {argumentos}".strip()