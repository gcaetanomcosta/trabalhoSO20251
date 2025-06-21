from .Instrucao import Instrucao


class ListaDeInstrucoes:
    def __init__(self, caminho_arquivo: str):
        self.instrucoes = []
        self.erros = []
        self._carregar_arquivo(caminho_arquivo)

    def _carregar_arquivo(self, caminho_arquivo: str):
        try:
            with open(caminho_arquivo, 'r') as arquivo:
                for numero_linha, linha in enumerate(arquivo, start=1):
                    linha = linha.strip()
                    if not linha or linha.startswith("#"):
                        continue
                    try:
                        partes = linha.split()
                        pid = partes[0]
                        tipo = partes[1]
                        args = partes[2:]
                        instrucao = Instrucao(pid, tipo, args)
                        self.instrucoes.append(instrucao)
                    except Exception as erro_instrucao:
                        msg_erro = f"Erro na linha {numero_linha}: '{linha}' -> {erro_instrucao}"
                        print(msg_erro)
                        self.erros.append(msg_erro)
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

    def __iter__(self):
        return iter(self.instrucoes)

    def __getitem__(self, index):
        return self.instrucoes[index]

    def __len__(self):
        return len(self.instrucoes)

    def __repr__(self):
        return f"ListaDeInstrucoes({len(self.instrucoes)} instruções carregadas)"