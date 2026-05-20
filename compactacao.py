"""
Arquivo responsável pela compactação dos índices.
"""

import os

import indices


def leia_reg(entrada):
    tam_bytes = entrada.read(2)
    tam_int = int.from_bytes(tam_bytes, "little")

    buffer_bytes = entrada.read(tam_int)
    buffer_str = buffer_bytes.decode("utf-8")

    if tam_int > 0:
        return buffer_str
    return ""


def atualizar_indice_primario(entrada):
    indice_id = []
    offset = 0
    buffer = leia_reg(entrada)
    while buffer != "":
        if buffer[0] != "*":
            campos = buffer.split("|")
            indice_id.append([int(campos[0]), offset])
        offset += 2 + len(buffer.encode("utf-8"))
        buffer = leia_reg(entrada)
    indice_id.sort()
    return indice_id


def compactar_arquivo(indice_id: list[list]):
    entrada = open("games.dat", "rb")
    saida = open("games_temp.dat", "wb")

    offset = 0  # Inicia o arquivo do começo
    buffer = leia_reg(entrada)

    while buffer != "":
        if buffer[0] != "*":
            # Escreve o registro no arquivo de saída
            tam_bytes = len(buffer).to_bytes(2, "little")
            saida.write(tam_bytes)
            saida.write(buffer.encode("utf-8"))
        offset += (
            2 + len(buffer)
        )  # Offset move para o próximo registro (tamanho do campo + tamanho do registro)
        buffer = leia_reg(entrada)

    atualizar_indice_primario(entrada)  # Atualiza o índice primário
    indices.salvar_indice(indice_id, "primario.ind")  # Salva o índice primário

    entrada.close()
    saida.close()
    os.remove("games.dat")  # Remove o arquivo original
    os.rename("games_temp.dat", "games.dat")  # Renomeia para games.dat
