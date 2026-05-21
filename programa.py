"""
Arquivo principal, executável que realiza as operações dependendo das flags passadas por linha de comando:
# -b -> lê o arquivo games.dat e constrói os índices lineares;
# -e -> carrega os índices e executa as operações especificadas;
# -c -> compacta o arquivo games.dat, removendo fisicamente os registros deletados.
"""

import sys

import compactacao
import indices
import operacoes


def main():
    flags = sys.argv

    listas = indices.carregar_indices()

    if flags[1] == "-b":
        try:
            open("games.dat", "rb")
        except FileNotFoundError:
            print("Arquivo de registros 'games.dat' não encontrado.")
            return

        listas = indices.criar_indices()

        # Salva os índices em arquivos de texto e a lista invertida em um arquivo de texto, seguindo o formato especificado
        indices.salvar_indice(listas[0], "primario.ind")
        indices.salvar_indice(listas[1], "genero.ind")
        indices.salvar_indice(listas[2], "publicadora.ind")
        indices.salvar_lista_invertida(listas[3], "lista_invertida.lst")

    elif flags[1] == "-e":
        try:
            open(f"{sys.argv[2]}.txt")
        except FileNotFoundError:
            print("Arquivo de operações não encontrado.")
            return

        arquivos_necessarios = [
            "genero.ind",
            "publicadora.ind",
            "primario.ind",
            "lista_invertida.lst",
        ]
        for arquivo in arquivos_necessarios:
            try:
                open(f"output/{arquivo}")
            except FileNotFoundError:
                print(f"O arquivo {arquivo} não foi encontrado.")
                return
        operacoes.realizar_operacao(f"{sys.argv[2]}.txt", listas)
    elif flags[1] == "-c":
        try:
            open("games.dat", "rb")
        except FileNotFoundError:
            print("Arquivo de registros 'games.dat' não encontrado.")
            return
        compactacao.compactar_arquivo(listas[0])
    return


if __name__ == "__main__":
    main()
