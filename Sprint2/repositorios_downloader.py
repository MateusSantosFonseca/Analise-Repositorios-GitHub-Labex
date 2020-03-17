from pygit2 import clone_repository
import os
import os.path
import shutil

# Este script depende da execução anterior do script sprint2.py, que gera um arquivo .txt chamado lista_url_repos, o qual é utilizado por este.

# ATENÇÃO: Para rodar esse script, vc tem que dar cd até o diretório \Sprint2, para, então, rodar o py repositorios_downloader.py
# caso contrário, as paths estarão erradas e você terá uma exception

repos_path = os.getcwd() + r"\Repositorios"
pathRelativa = os.getcwd() + r"\lista_urls_repos.txt"
path = repos_path

# Remove o diretorio \Repositorios e seu conteudo, porém nem sempre funciona ainda, não se porque. Portanto, mantenha sempre
# o diretório \Repositorios removido, juntamente com os repositórios baixados nele.
try:
    shutil.rmtree(path)
except:
    print(r"O diretório \Repositorios não pode ser excluido pois ele não existe.")

try:
    os.mkdir(repos_path)
    print("Diretorio ", repos_path, " criado ")
except FileExistsError:
    print("Diretorio:", repos_path, "já existe")

try:
    with open(pathRelativa) as file:
        urls_nomes_list = list(file)
except:
    print("Ocorreu um problema na execução do script, o arquivo não pode ser lido")

countRepositorionsBaixados = 0

# Baixa os repositórios seguindo a ordem do arquivo texto lista_urls_repos.
# Cria um index no sufixo de cada diretorio de repositorio para fins de ordenacao
for url_repo in urls_nomes_list:
    countRepositorionsBaixados += 1
    array_url_nome = url_repo.split(',')
    nome_repositorio = array_url_nome[1].strip()
    path_repo_baixado = path + "\\" + "{:04n}".format(countRepositorionsBaixados) + "_" + nome_repositorio
    if not os.path.exists(path_repo_baixado):
        os.mkdir(path_repo_baixado)
        print("Voce está baixando o repositorio: " + nome_repositorio)
        repo = clone_repository(array_url_nome[0].strip(), path_repo_baixado, bare=False)
    else:
        print("O repositório: " + nome_repositorio + " ja foi baixado!!")

print("\nTodos repositórios foram baixados com sucesso!")