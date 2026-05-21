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


def busca_binaria_indice(x: str | int, lista: list) -> int:
    i = 0
    f = len(lista) - 1
    while i <= f:
        m = (i + f) // 2
        if lista[m][0] == x:
            return m
        if lista[m][0] < x:
            i = m + 1
        else:
            f = m - 1
    return -1


def busca_offset(offset: int) -> str:
    with open("games.dat", "rb") as arq:
        arq.seek(offset)
        tam = int.from_bytes(arq.read(2), "little")
        if tam > 0:
            reg_string = arq.read(tam)
            return reg_string.decode()
        return ""


def busca_primaria(id: int, index_primario: list[list[int]]) -> str:
    offset = busca_binaria_indice(id, index_primario)
    if offset == -1:
        return f"Registro com ID '{id}' não encontrado."
    else:
        return busca_offset(index_primario[offset][1])


def busca_secundaria(
    chave: str,
    index_secundario: list,
    index_primario: list,
    lista_invertida: list,
    indice_lista_invertida: int = 1,
) -> list[int]:
    resultado = []
    rrn = busca_binaria_indice(chave, index_secundario)
    if rrn == -1:
        print(f"Nenhum registro com '{chave}' não encontrado.")
    else:
        prox_gen = index_secundario[rrn][1]
        while prox_gen != -1:
            resultado.append(
                busca_primaria(int(lista_invertida[prox_gen][0]), index_primario)
            )
            prox_gen = lista_invertida[prox_gen][indice_lista_invertida]

    return resultado


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
    index_primario, index_genero, index_publicadora, lista_invertida = listas
    with open(arquivo, "r") as file:
        for linha in file:
            operacao = identificar_operacao(linha)
            argumento = identificar_argumentos(linha)
            match operacao:
                case "bp":
                    print(f"Busca pelo registro de ID '{argumento}'")
                    registro = busca_primaria(int(argumento), index_primario)
                    print(registro)
                case "bs1":
                    print(f"Busca por registros de gênero '{argumento}'")
                    registros = busca_secundaria(
                        argumento, index_genero, index_primario, lista_invertida
                    )
                    print(f"Foram encontrados {len(registros)} registros: ")
                    for registro in registros:
                        print(registro)
                case "bs2":
                    print(f"Busca por registros da publicadora '{argumento}'")
                    registros = busca_secundaria(
                        argumento, index_publicadora, index_primario, lista_invertida, 2
                    )
                    print(f"Foram encontrados {len(registros)} registros: ")
                    for registro in registros:
                        print(registro)
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
