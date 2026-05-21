"""
Arquivo responsável pela compactação dos índices.
"""

import os

import indices


def compactar_arquivo(indice_id: list[list]):
    entrada = open("games.dat", "rb")
    saida = open("games_temp.dat", "wb")

    indice_id = []
    offset = 0
    buffer = indices.leia_reg(entrada)

    while buffer != "":
        if buffer[0] != "*":
            # Escreve o registro no arquivo de saída
            tam_bytes = len(buffer).to_bytes(2, "little")
            saida.write(tam_bytes)
            saida.write(buffer.encode("utf-8"))
            indice_id.append([int(buffer.split("|")[0]), offset])
            offset += 2 + len(buffer.encode("utf-8"))
        buffer = indices.leia_reg(entrada)

    indices.salvar_indice(indice_id, "primario.ind")  # Salva o índice primário

    entrada.close()
    saida.close()
    os.remove("games.dat")  # Remove o arquivo original
    os.rename("games_temp.dat", "games.dat")  # Renomeia para games.dat
