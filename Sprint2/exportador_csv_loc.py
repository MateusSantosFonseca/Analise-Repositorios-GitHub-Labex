import os
from glob import glob
from csv import writer
import fileinput, sys, csv
import csv

# A base deste código foi retirado de uma resposta do usuário Bryce93 no fórum StackOverFlow
# https://stackoverflow.com/questions/38543709/count-lines-of-code-in-directory-using-python/38543710#38543710

root_path = os.getcwd()

def countlines(start, lines=0, header=True, begin_start=None):
    try:
        for thing in os.listdir(start):
            thing = os.path.join(start, thing)
            if os.path.isfile(thing):
                if thing.endswith('.py'):
                    with open(thing, 'r') as f:
                        newlines = f.readlines()
                        newlines = len(newlines)
                        lines += newlines

                        if begin_start is not None:
                            reldir_of_thing = '.' + thing.replace(begin_start, '')
                        else:
                            reldir_of_thing = '.' + thing.replace(start, '')

        for thing in os.listdir(start):
            thing = os.path.join(start, thing)
            if os.path.isdir(thing):
                lines = countlines(thing, lines, header=False, begin_start=start)
    except:
        pass

    return lines

# Esta funcao é responsável por ler os valores do .csv antigo e adicionar a nova coluna "Lines of code" calculada. Um outro arquivo .csv
# com esta coluna é criada
def concatenador_CSV(vetor_locs):
    csv_readed_file_path = root_path + r"\output_repositorios_github.csv"
    with open(csv_readed_file_path, mode='r') as csv_file:
        with open(root_path + r"\output_repositorios_github_sprint2.csv", mode='w+') as csv_final_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            csv_final_writer = csv.writer(csv_final_file)
            isHeader = True
            indice_LOCS = 0
            for row in csv_reader:
                if len(row) != 0:
                    if isHeader is not True:
                        csv_final_writer.writerow([row[0]] + [row[1]] + [row[2]] + [row[3]] + [row[4]] + [row[5]] + [" " + str(vetor_locs[indice_LOCS])] + [row[6]])
                        indice_LOCS += 1
                    else:
                        header = (["Nome", "Linguagem primária", "Quantidade de stars", "Watchers", "Data de criação", "Quantidade de forks", "Lines of Code", "URL"])
                        csv_final_writer.writerow(header)
                        isHeader = False
    
    try:
        os.remove(csv_readed_file_path)
    except:
        print("Erro ao deletar o arquivo: ", csv_readed_file_path)


repos_path =  os.getcwd() + r"\Repositorios\*\\"

diretorios = glob(repos_path)

vetor_locs = []

# Calculando o LOC para cada repositorio em \Repositorios
for repo_diretorio in diretorios:
    quantidade_linhas_repo = (countlines(repo_diretorio))
    vetor_locs.append(quantidade_linhas_repo)
    
concatenador_CSV(vetor_locs)
