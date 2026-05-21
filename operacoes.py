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
    rrn_index = busca_binaria_indice(chave, index_secundario)
    if rrn_index == -1:
        print(f"Nenhum registro com '{chave}' não encontrado.")
    else:
        prox = index_secundario[rrn_index][1]
        while prox != -1:
            if lista_invertida[prox][0] != "*":
                resultado.append(busca_primaria(int(lista_invertida[prox][0]), index_primario))
            prox = lista_invertida[prox][indice_lista_invertida]

    return resultado


def remover_jogo(arg_id: int, index_primario: list[list], lista_invertida: list[list]) -> None:
    rrn_index = busca_binaria_indice(arg_id, index_primario)  # Retorna -1 se não encontrar o arg_id
    offset = index_primario[rrn_index][1]

    if rrn_index == -1:
        print(f"Jogo com ID '{arg_id}' não encontrado.")
        return
    else:
        print(f"Removendo jogo com ID '{arg_id}' no offset {offset}.")

        entrada = open("games.dat", "rb+")
        entrada.seek(offset + 2)  # Pula o tamanho do registro

        marcador = "*"
        marcador_bytes = marcador.encode("utf-8")  # Converte o marcador para bytes
        entrada.write(marcador_bytes)  # Marca o registro como deletado, usando '*' como indicador

        entrada.close()

        index_primario.pop(rrn_index)  # Remove o jogo do índice primário

        for i in range(len(lista_invertida)):
            if int(lista_invertida[i][0]) == arg_id:
                lista_invertida[i][0] = "*"

        indices.salvar_indice(index_primario, "primario.ind")
        indices.salvar_lista_invertida(lista_invertida, "lista_invertida.lst")
    return


def inserir_jogo(jogo: str, index_primario, index_genero, index_publicadora, lista_invertida) -> None:
    campos = jogo.split("|")
    id_jogo = int(campos[0])
    genero = campos[3]
    publicadora = campos[4]

    rrn_index = busca_binaria_indice(id_jogo, index_primario)  # Retorna -1 se não encontrar o arg_id

    if rrn_index != -1:
        print(f"ID '{id_jogo}' já existe. Inserção cancelada.")
        return

    reg_bytes = jogo.encode("utf-8")

    tam_int = len(reg_bytes)
    tam_bytes = tam_int.to_bytes(2, "little")
    print(f"Inserindo jogo com ID {id_jogo} e {tam_int} bytes.")

    saida = open("games.dat", "ab")

    saida.write(tam_bytes)
    saida.write(reg_bytes)

    offset = saida.tell() - (2 + tam_int)
    saida.close()

    index_primario.append([id_jogo, offset])

    rrn = len(lista_invertida)
    registro_inv = [campos[0], -1, -1]

    prox_genero = indices.encontra_posicao(index_genero, genero, rrn, lista_invertida, id_jogo, 1)
    prox_pub = indices.encontra_posicao(index_publicadora, publicadora, rrn, lista_invertida, id_jogo, 2)

    registro_inv = [id_jogo, prox_genero, prox_pub]
    lista_invertida.append(registro_inv)

    index_primario.sort()
    index_genero.sort()
    index_publicadora.sort()

    indices.salvar_indice(index_primario, "primario.ind")
    indices.salvar_indice(index_genero, "genero.ind")
    indices.salvar_indice(index_publicadora, "publicadora.ind")
    indices.salvar_lista_invertida(lista_invertida, "lista_invertida.lst")
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
                    print("\n")
                case "bs1":
                    print(f"Busca por registros de gênero '{argumento}'")
                    registros = busca_secundaria(argumento, index_genero, index_primario, lista_invertida)
                    print(f"Foram encontrados {len(registros)} registros: ")
                    for registro in registros:
                        print(registro)
                    print("\n")
                case "bs2":
                    print(f"Busca por registros da publicadora '{argumento}'")
                    registros = busca_secundaria(argumento, index_publicadora, index_primario, lista_invertida, 2)
                    print(f"Foram encontrados {len(registros)} registros: ")
                    for registro in registros:
                        print(registro)
                    print("\n")
                case "i":
                    print("Realizando inserção de um novo registro")
                    inserir_jogo(argumento, index_primario, index_genero, index_publicadora, lista_invertida)
                    print("\n")
                case "r":
                    print("Realizando remoção lógica de um registro")
                    remover_jogo(int(argumento), index_primario, lista_invertida)
                    print("\n")
                case _:
                    print(f"Operação {operacao} não encontrada, prosseguindo para a próxima.")
