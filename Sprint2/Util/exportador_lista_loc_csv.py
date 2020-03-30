import os
from glob import glob
from csv import writer
import fileinput, sys, csv
import csv

# Esta funcao é responsável por ler os valores do .csv antigo e adicionar a nova coluna "Lines of code" calculada. Um outro arquivo .csv
# com esta coluna é criada
def concatenador_CSV(vetor_locs, root_path):
    csv_readed_file_path = root_path + r"\output_repositorios_github.csv"
    with open(csv_readed_file_path, mode='r') as csv_file:
        with open(root_path + r"\output_dados_repositorios.csv", mode='w+') as csv_final_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            csv_final_writer = csv.writer(csv_final_file)
            isHeader = True
            indice_LOCS = 0
            for row in csv_reader:
                if len(row) != 0:
                    if isHeader is not True:
                        locAtual = [" " + str(vetor_locs[indice_LOCS].rstrip("\n"))]
                        csv_final_writer.writerow([row[0]] + [row[1]] + [row[2]] + [row[3]] + [row[4]] + [row[5]] + locAtual + [row[6]])
                        indice_LOCS += 1
                    else:
                        header = (["Nome", "Linguagem primária", "Quantidade de stars", "Watchers", "Data de criação", "Quantidade de forks", "Lines of Code", "URL"])
                        csv_final_writer.writerow(header)
                        isHeader = False
    
    try:
        os.remove(csv_readed_file_path)
    except:
        print("Erro ao deletar o arquivo: ", csv_readed_file_path)

def runExportadorListaLocCsvScriptMain(fase_atual):
    root_path = os.getcwd() + fase_atual
    pathRelativaListaLocs = root_path + r"\lista_locs_repos.txt"

    try:
        with open(pathRelativaListaLocs) as file:
            vetor_locs = list(file)
    except:
        print("Ocorreu um problema na execução do script, o arquivo .txt que contém os LOCS não pode ser lido")
        
    concatenador_CSV(vetor_locs, root_path)