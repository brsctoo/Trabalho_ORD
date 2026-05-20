"""
Arquivo responsável pelas operações nos índices lineares:
# primário: índice pelo ID do jogo;
# gênero: índice secundário por gênero;
# publicadora: índice secundário por publicadora;

Além da construção, cuida do carregamento, salvamento e atualização dos índices em memória.

Obs. Para os índices secundários, é usado lista invertida com late binding.
"""


def identificar_operacao(linha: str) -> str:
    return linha.strip().split(" ", 1)[0]


def identificar_argumentos(linha: str) -> str:
    return linha.strip().split(" ", 1)[1]


def busca_offset(offset: int) -> str:
    with open("games.dat", "rb") as arq:
        arq.seek(offset)
        tam = int.from_bytes(arq.read(2), "little")
        if tam > 0:
            reg_string = arq.read(tam)
            return reg_string.decode()
        return ""


def busca_primaria(id: int) -> str:
    lista_indices = []
    with open("output/primario.ind", "r") as index_primario:
        for linha in index_primario:
            campos = linha.split("|")
            id_primario = int(campos[0])
            ref_offset = int(campos[1])
            lista_indices.append([id_primario, ref_offset])
    for i in range(len(lista_indices)):
        if lista_indices[i][0] == id:
            registro = busca_offset(lista_indices[i][1])
            return registro
    else:
        return f"Registro de ID '{id}' não encontrado."


def realizar_operacao(arquivo: str, listas: tuple) -> None:
    with open(arquivo, "r") as file:
        for linha in file:
            operacao = identificar_operacao(linha)
            argumento = identificar_argumentos(linha)
            match operacao:
                case "bp":
                    print(f"Busca pelo registro de ID '{argumento}'")
                    print(busca_primaria(int(argumento)))

                case "bs1":
                    print("Realizando busca pelo índice secundário de gênero")
                case "bs2":
                    print("Realizando busca pelo índice secundário de publicadora")
                case "i":
                    print("Realizando inserção de um novo registro")
                case "r":
                    print("Realizando remoção lógica de um registro")
                case _:
                    print(
                        f"Operação {operacao} não encontrada, prosseguindo para a próxima."
                    )
