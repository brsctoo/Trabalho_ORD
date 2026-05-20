"""
Arquivo responsável pelas operações nos índices lineares:
# primário: índice pelo ID do jogo;
# gênero: índice secundário por gênero;
# publicadora: índice secundário por publicadora;

Além da construção, cuida do carregamento, salvamento e atualização dos índices em memória.

Obs. Para os índices secundários, é usado lista invertida com late binding.
"""

import indices


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


def remover_jogo(
    arg_id: int, indice_id: list[list], lista_invertida: list[list]
) -> None:
    offset = -1
    idx_remover = -1

    for i in range(len(indice_id)):
        if int(indice_id[i][0]) == arg_id:
            offset = indice_id[i][1]
            idx_remover = i
            break

    if offset == -1:
        print(f"Jogo com ID '{arg_id}' não encontrado.")
        return
    else:
        print(f"Removendo jogo com ID '{arg_id}' no offset {offset}.")

        entrada = open("games.dat", "rb+")
        entrada.seek(offset + 2)  # Pula o tamanho do registro (2 bytes)

        marcador = "*"
        marcador_bytes = marcador.encode("utf-8")  # Converte o marcador para bytes
        entrada.write(
            marcador_bytes
        )  # Marca o registro como deletado, usando '*' como indicador

        entrada.close()

        indice_id.pop(idx_remover)  # Remove o jogo do índice primário

        for i in range(len(lista_invertida)):
            if int(lista_invertida[i][0]) == arg_id:
                lista_invertida[i][0] = "*"

        indices.salvar_indice(indice_id, "primario.ind")
        indices.salvar_lista_invertida(lista_invertida, "lista_invertida.lst")
    return


def inserir_jogo(jogo: str, listas: tuple) -> None:
    # Função para inserir um novo jogo, seguindo o formato de registro especificado
    # O registro deve ser inserido no final do arquivo 'games.dat' e os índices devem ser atualizados

    indice_id = listas[0]

    campos = jogo.split("|")
    id_jogo = int(campos[0])

    for item in indice_id:
        if int(item[0]) == id_jogo:
            print(f"ID '{id_jogo}' já existe. Inserção cancelada.")
            return

    reg_bytes = jogo.encode("utf-8")

    tam_int = len(reg_bytes)
    tam_bytes = tam_int.to_bytes(2, "little")
    print(f"Inserindo jogo com ID '{id_jogo}' no final do arquivo.")

    saida = open("games.dat", "ab")
    saida.write(tam_bytes)  # Escreve o tamanho do registro (2 bytes)
    saida.write(reg_bytes)  # Escreve o registro em bytes no final do arquivo
    saida.close()

    return


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
                    inserir_jogo(argumento, listas)
                case "r":
                    print("Realizando remoção lógica de um registro")
                    remover_jogo(int(argumento), listas[0], listas[3])
                case _:
                    print(
                        f"Operação {operacao} não encontrada, prosseguindo para a próxima."
                    )
