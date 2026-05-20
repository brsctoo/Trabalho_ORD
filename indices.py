"""
Arquivo responsável pela construção, buscas, inserção e remoção nos índices:
# bp -> busca um registro pelo índice primário (ID);
# bs1 -> busca registros pelo índice secundário de gênero;
# bs2 -> busca registros pelo índice secundário de publicadora;
# i -> insere um novo registro no arquivo games.dat e atualiza os índices;
# r -> remove logicamente um registro do arquivo games.dat e atualiza os índices.
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


def criar_indices():
    # Lê o arquivo games.dat e constrói os quatro índices em memória

    indice_id = []
    indice_gen = []
    indice_pub = []
    lista_invertida = []

    entrada = open("games.dat", "rb")

    offset = 0  # Inicia o arquivo do começo
    buffer = leia_reg(entrada)

    while buffer != "":
        if buffer[0] != "*":
            # Divide o campo com a função split e guarda os dados em variáveis
            campos = buffer.split("|")
            jogo_id = campos[0]
            genero = campos[3]
            publicadora = campos[4]

            rnn_atual = len(indice_id)  # Posição do registro atual no índice primário
            indice_id.append([int(jogo_id), int(offset)])
            registro_inv = [jogo_id, -1, -1]  # Registro para a lista invertida

            # Se o gênero está na lista de gêneros:
            # - Chave primária na lista invertida -> aponta para o rnn do último registro com o mesmo gênero.
            # Se o gênero não está na lista de gêneros:
            # - Adicionamos ele na lista de gênero, com referência ao rnn atual;
            # - Chave primária na lista invertida -> aponta para -1.

            idx_gen = -1  # Index de onde o gênero está na lista de gêneros
            for i in range(len(indice_gen)):
                if indice_gen[i][0] == genero:
                    idx_gen = i
                    break

            # Está na lista
            if idx_gen != -1:
                registro_inv[1] = indice_gen[idx_gen][
                    1
                ]  # O novo aponta para o velho -> Entra na cabeça da lista
                indice_gen[idx_gen][1] = (
                    rnn_atual  # O genêro no indice_gen agora aponta pro o novo
                )
            else:
                # Não está na lista
                indice_gen.append([genero, rnn_atual])

            # Se a publicadora está na lista de publicadoras:
            # - Chave primária na lista invertida -> aponta para o rnn do último registro com a mesma publicadora.
            # Se a publicadora não está na lista de publicadoras:
            # - Adicionamos ele na lista de publicadoras, com referência ao rnn atual;
            # - Chave primária na lista invertida -> aponta para -1.

            idx_pub = -1  # Index de onde a publicadora está na lista de publicadoras
            for i in range(len(indice_pub)):
                if indice_pub[i][0] == publicadora:
                    idx_pub = i
                    break

            # Está na lista
            if idx_pub != -1:
                registro_inv[2] = indice_pub[idx_pub][
                    1
                ]  # O novo aponta para o velho -> Entra na cabeça da lista
                indice_pub[idx_pub][1] = (
                    rnn_atual  # O genêro no indice_gen agora aponta pro o novo
                )
            else:
                # Não está na lista
                indice_pub.append([publicadora, rnn_atual])

            lista_invertida.append(
                registro_inv
            )  # Adiciona o registro invertido na lista invertida

        offset += 2 + len(buffer.encode("utf-8"))  # Atualiza o offset
        buffer = leia_reg(entrada)

    indice_id.sort()  # Ordena o índice primário por ID
    indice_gen.sort()  # Ordena o índice secundário de gênero por gênero
    indice_pub.sort()  # Ordena o índice secundário de publicadora por publicadora

    entrada.close()

    return (indice_id, indice_gen, indice_pub, lista_invertida)


def salvar_indices(indice_id, indice_gen, indice_pub, lista_invertida):
    # Salva os índices em arquivos de texto, seguindo o formato especificado:
    # primário.ind -> id|offset
    # genero.ind -> genero|rrn
    # publicadora.ind -> publicadora|rrn
    # lista_invertida.lst -> id|prox_gen|prox_pub

    os.makedirs("output", exist_ok=True)

    saida = open("output/primario.ind", "w")
    for i in range(len(indice_id)):
        chave = indice_id[i][0]
        offset = str(indice_id[i][1])
        saida.write(
            str(chave) + "|" + offset + "\n"
        )  # Escreve no primario.ind -> id|offset
    saida.close()

    saida = open("output/genero.ind", "w", encoding="utf-8")
    for i in range(len(indice_gen)):
        genero = indice_gen[i][0]
        rrn = str(indice_gen[i][1])
        saida.write(genero + "|" + rrn + "\n")  # Escreve no genero.ind -> genero|rrn
    saida.close()

    saida = open("output/publicadora.ind", "w", encoding="utf-8")
    for i in range(len(indice_pub)):
        publicadora = indice_pub[i][0]
        rrn = str(indice_pub[i][1])
        saida.write(
            publicadora + "|" + rrn + "\n"
        )  # Escreve no publicadora.ind -> publicadora|rrn
    saida.close()

    saida = open("output/lista_invertida.lst", "w", encoding="utf-8")
    for i in range(len(lista_invertida)):
        jogo_id = lista_invertida[i][0]
        prox_gen = str(lista_invertida[i][1])
        prox_pub = str(lista_invertida[i][2])
        saida.write(
            jogo_id + "|" + prox_gen + "|" + prox_pub + "\n"
        )  # Escreve no lista_invertida.lst -> id|prox_gen|prox_pub
    saida.close()


def carregar_indices():
    # Carrega os índices dos arquivos de texto para estruturas de dados em memória, seguindo o formato especificado

    with open("output/primario.ind", "r") as indice_pimario:
        indice_id = []
        for linha in indice_pimario:
            campos = linha.strip().split("|")
            indice_id.append(
                [campos[0], int(campos[1])]
            )  # Lê o primário.ind -> id|offset:

    with open("output/genero.ind", "r", encoding="utf-8") as indice_secundario_genero:
        indice_gen = []
        for linha in indice_secundario_genero:
            campos = linha.strip().split("|")
            indice_gen.append(
                [campos[0], int(campos[1])]
            )  # Lê o genero.ind -> genero|rrn

    with open(
        "output/publicadora.ind", "r", encoding="utf-8"
    ) as indice_secundario_publicadora:
        indice_pub = []
        for linha in indice_secundario_publicadora:
            campos = linha.strip().split("|")
            indice_pub.append(
                [campos[0], int(campos[1])]
            )  # Lê o publicadora.ind -> publicadora|rrn

    with open(
        "output/lista_invertida.lst", "r", encoding="utf-8"
    ) as lista_invertida_file:
        lista_invertida = []
        for linha in lista_invertida_file:
            campos = linha.strip().split("|")
            lista_invertida.append(
                [campos[0], int(campos[1]), int(campos[2])]
            )  # Lê o lista_invertida.lst -> id|prox_gen|prox_pub
    return (indice_id, indice_gen, indice_pub, lista_invertida)
