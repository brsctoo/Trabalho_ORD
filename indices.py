"""
Arquivo responsável pelas operações nos índices lineares:
# primário: índice pelo ID do jogo;
# gênero: índice secundário por gênero;
# publicadora: índice secundário por publicadora;

Além da construção, cuida do carregamento, salvamento e atualização dos índices em memória.

Obs. Para os índices secundários, é usado lista invertida com late binding.
"""

import os


def leia_reg(entrada):
    tam_bytes = entrada.read(2)
    tam_int = int.from_bytes(tam_bytes, "little")

    buffer_bytes = entrada.read(tam_int)
    buffer_str = buffer_bytes.decode("utf-8")

    if tam_int > 0:
        return buffer_str
    return ""


def encontra_posicao(
    index_chave: list, chave_secundaria: str, rrn_jogo: int, lista_invertida: list, id: int, coluna: int
) -> int:
    prox = -1

    # Procura se já está no índice secundário de gênero
    posicao_chave = -1
    for i in range(len(index_chave)):
        if index_chave[i][0] == chave_secundaria:
            posicao_chave = i  # Posição no índice
            break

    if posicao_chave != -1:  # Se está no índice
        # RRN que o gênero aponta -> Começa pelo RRN do índice
        rrn_apontado = int(index_chave[posicao_chave][1])
        rrn_anterior = -1

        while rrn_apontado != -1:
            marcador = "*"

            id_comparado = lista_invertida[rrn_apontado][0]
            if str(id_comparado) != marcador:
                if int(id_comparado) > int(id):
                    break

            # Se o ID jogador é maior ou o registro foi removido, ele o RRN como anterior e vai pro próximo
            rrn_anterior = rrn_apontado
            rrn_apontado = int(lista_invertida[rrn_apontado][coluna])

        prox = rrn_apontado

        # Se for o menor, coloca na cabeça. Se não, coloca no lugar certo.
        if rrn_anterior == -1:
            index_chave[posicao_chave][1] = rrn_jogo
        else:
            lista_invertida[rrn_anterior][coluna] = rrn_jogo
    else:
        index_chave.append([chave_secundaria, rrn_jogo])

    return prox


def criar_indices():
    index_id = []
    index_genero = []
    index_publicadora = []
    lista_invertida = []

    entrada = open("games.dat", "rb")

    offset = 0
    buffer_registro = leia_reg(entrada)

    while buffer_registro != "":
        if buffer_registro[0] != "*":
            campos = buffer_registro.split("|")
            id = int(campos[0])
            genero = campos[3]
            publicadora = campos[4]

            rrn_jogo = len(index_id)
            index_id.append([int(id), int(offset)])

            prox_genero = encontra_posicao(index_genero, genero, rrn_jogo, lista_invertida, id, 1)
            prox_pub = encontra_posicao(index_publicadora, publicadora, rrn_jogo, lista_invertida, id, 2)

            registro_invertido = [id, prox_genero, prox_pub]

            lista_invertida.append(registro_invertido)

        offset += 2 + len(buffer_registro.encode("utf-8"))
        buffer_registro = leia_reg(entrada)

    index_id.sort()
    index_genero.sort()
    index_publicadora.sort()

    entrada.close()

    return (index_id, index_genero, index_publicadora, lista_invertida)


def salvar_indice(indice: list, nome_arq: str):
    # Salva o índice em arquivos de texto, de nome nome_arq
    # Seguindo o formato especificado:
    # primário.ind -> id|offset
    # genero.ind -> genero|rrn
    # publicadora.ind -> publicadora|rrn

    os.makedirs("output", exist_ok=True)

    saida = open(f"output/{nome_arq}", "w")
    for i in range(len(indice)):
        chave = indice[i][0]
        ref = str(indice[i][1])
        saida.write(str(chave) + "|" + ref + "\n")  # Escreve no arquivo
    saida.close()


def salvar_lista_invertida(lista_invertida: list, nome_arq: str):
    # Salva a lista invertida em arquivos de texto de nome nome_arq

    os.makedirs("output", exist_ok=True)

    saida = open(f"output/{nome_arq}", "w", encoding="utf-8")
    for i in range(len(lista_invertida)):
        jogo_id = lista_invertida[i][0]
        prox_gen = str(lista_invertida[i][1])
        prox_pub = str(lista_invertida[i][2])
        saida.write(
            str(jogo_id) + "|" + prox_gen + "|" + prox_pub + "\n"
        )  # Escreve no arquivo texto -> id|prox_gen|prox_pub
    saida.close()


def carregar_indices():
    # Carrega os índices dos arquivos de texto para estruturas de dados em memória, seguindo o formato especificado

    with open("output/primario.ind", "r") as indice_pimario:
        index_primario = []
        for linha in indice_pimario:
            campos = linha.strip().split("|")
            index_primario.append([int(campos[0]), int(campos[1])])  # Lê o primário.ind -> id|offset:

    with open("output/genero.ind", "r", encoding="utf-8") as indice_secundario_genero:
        index_genero = []
        for linha in indice_secundario_genero:
            campos = linha.strip().split("|")
            index_genero.append([campos[0], int(campos[1])])  # Lê o genero.ind -> genero|rrn

    with open("output/publicadora.ind", "r", encoding="utf-8") as indice_secundario_publicadora:
        index_publicadora = []
        for linha in indice_secundario_publicadora:
            campos = linha.strip().split("|")
            index_publicadora.append([campos[0], int(campos[1])])  # Lê o publicadora.ind -> publicadora|rrn

    with open("output/lista_invertida.lst", "r", encoding="utf-8") as lista_invertida_file:
        lista_invertida = []
        for linha in lista_invertida_file:
            campos = linha.strip().split("|")
            lista_invertida.append(
                [campos[0], int(campos[1]), int(campos[2])]
            )  # Lê o lista_invertida.lst -> id|prox_gen|prox_pub
    return (index_primario, index_genero, index_publicadora, lista_invertida)
