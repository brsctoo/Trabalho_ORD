"""
Arquivo principal, executável que realiza as operações dependendo das flags passadas por linha de comando:
# -b -> lê o arquivo games.dat e constrói os índices lineares;
# -e -> carrega os índices e executa as operações especificadas;
# -c -> compacta o arquivo games.dat, removendo fisicamente os registros deletados.
"""

import sys

import indices
import operacoes


def main():
    flags = sys.argv

    if flags[1] == "-b":
        try:
            open("games.dat", "rb")
        except FileNotFoundError:
            print("Arquivo de registros 'games.dat' não encontrado.")
            return
        listas = indices.criar_indices()
        indices.salvar_indices(listas[0], listas[1], listas[2], listas[3])

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
        operacoes.realizar_operacao(f"{sys.argv[2]}.txt")
    return


if __name__ == "__main__":
    main()
