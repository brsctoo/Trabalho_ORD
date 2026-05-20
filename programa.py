'''
Arquivo principal, executável que realiza as operações dependendo das flags passadas por linha de comando:
# -b -> lê o arquivo games.dat e constrói os índices lineares;
# -e -> carrega os índices e executa as operações especificadas;
# -c -> compacta o arquivo games.dat, removendo fisicamente os registros deletados.
'''

import sys
import operacoes
import indices

def main():
    flag = sys.argv[1]

    if flag == "-b":
        listas = indices.criar_indices()
        indices.salvar_indices(listas[0], listas[1], listas[2], listas[3])
    return

if __name__ == "__main__":
    main()
