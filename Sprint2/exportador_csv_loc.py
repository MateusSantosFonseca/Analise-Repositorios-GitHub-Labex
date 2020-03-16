import os
from glob import glob
from csv import writer
import fileinput, sys, csv

# A base deste código foi retirado de uma resposta do usuário Bryce93 no fórum StackOverFlow
# https://stackoverflow.com/questions/38543709/count-lines-of-code-in-directory-using-python/38543710#38543710

def countlines(start, lines=0, header=True, begin_start=None):
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

    return lines


repos_path =  os.getcwd() + r"\Repositorios\*\\"
diretorios = glob(repos_path)


# Neste loop, fazer alguma logica que concatena em cada linha do arquivo .csv existente: "," + quantidade_linhas_repo.
# Além disso, na primeira linha do .csv, deve adicionar: ",Linhas de Código do Repositório"
# OBS.: Como os diretorios estao ordenados e com o index ao lado,
# nao preciso preocupar com a ordem de inserção da metrica LOC, ela vai ser sempre inserida corretamente
# OBS.: Lembrar de pular linhas brancas de alguma forma

# Inserir na row header a coluna LOC aqui
for repo_diretorio in diretorios:
    quantidade_linhas_repo = (countlines(repo_diretorio))
    # Concatenar na linha do .csv: "," + quantidade_linhas_repo
    