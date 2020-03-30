from pygit2 import clone_repository
import os, stat
import os.path
import shutil

# Este script depende da execução anterior do script sprint2.py, que gera um arquivo .txt chamado lista_url_repos, o qual é utilizado por este.

# ATENÇÃO: Para rodar esse script, vc tem que dar cd até o diretório \Sprint2, para, então, rodar o py repositorios_downloader.py
# caso contrário, as paths estarão erradas e você terá uma exception

def contadorQuantidadeLinhasArquivosPy(start, lines=0, header=True, begin_start=None):
    try:
        for arquivo in os.listdir(start):
            arquivo = os.path.join(start, arquivo)
            if os.path.isfile(arquivo):
                if arquivo.endswith('.py'):
                    with open(arquivo, 'r') as f:
                        newlines = f.readlines()
                        newlines = len(newlines)
                        lines += newlines

                        if begin_start is not None:
                            reldir_of_thing = '.' + arquivo.replace(begin_start, '')
                        else:
                            reldir_of_thing = '.' + arquivo.replace(start, '')

        for arquivo in os.listdir(start):
            arquivo = os.path.join(start, arquivo)
            if os.path.isdir(arquivo):
                lines = contadorQuantidadeLinhasArquivosPy(arquivo, lines, header=False, begin_start=start)
    except:
        pass

    return lines

# Chama-se a funcao para abrir a todo momento devido a possibilidade de crash na execução de download de repositorios
def exportarLocsParaTXT(listaLocs, pathRelativaArquivoLocs):
    file = open(pathRelativaArquivoLocs, "w+")  
    file.write(listaLocs)
    file.close

def excluirPasta(diretorio):
    try:
        shutil.rmtree(diretorio)
    except:
        print(r"O diretório: " + diretorio + " não pode ser excluido. Favor apagá-lo manualmente.")


# Remove o diretorio \Repositorios e seu conteudo, porém nem sempre funciona ainda, não sei porque. Portanto, mantenha sempre
# o diretório \Repositorios removido, juntamente com os repositórios baixados nele.

def runScriptDownloaderContadorLocsRepositoriosMain(fase_atual):
    repos_path = os.getcwd() + r"\Repositorios"
    pathRelativaArquivoUrls = os.getcwd() + fase_atual +  r"\lista_urls_repos.txt"
    pathRelativaArquivoLocs = os.getcwd() + fase_atual + r"\lista_locs_repos.txt"
    path = repos_path

    desejaManterReposBaixados = False # Define se os repos ficarão baixados ou serão apagados apos análise de LOCS
    excluirPasta(path)
    urls_nomes_list = ""

    try:
        os.mkdir(repos_path)
        print("\nDiretorio ", repos_path, "criado ")
    except FileExistsError:
        print("\nDiretorio:", repos_path, "já existe")

    try:
        with open(pathRelativaArquivoUrls) as file:
            urls_nomes_list = list(file)
    except:
        print("Ocorreu um problema na execução do script, o arquivo não pode ser lido")

    countRepositorionsBaixados = 0
    listaLocs = ""

    # Baixa os repositórios seguindo a ordem do arquivo texto lista_urls_repos.
    # Cria um index no sufixo de cada diretorio de repositorio para fins de ordenacao
    for url_repo in urls_nomes_list:
        countRepositorionsBaixados += 1
        array_url_nome = url_repo.split(',')
        nome_repositorio = array_url_nome[1].strip()
        path_repo_baixado = path + "\\" + "{:04n}".format(countRepositorionsBaixados) + "_" + nome_repositorio
        
        if not os.path.exists(path_repo_baixado):
            os.mkdir(path_repo_baixado)
            print("Voce está baixando o repositorio: " + nome_repositorio + " ele é o " + str(countRepositorionsBaixados) + "° repositório baixado.")
            clone_repository(array_url_nome[0].strip(), path_repo_baixado, bare=False)
        else:
            print("O repositório: " + nome_repositorio + " já foi baixado!!")
        listaLocs += str(contadorQuantidadeLinhasArquivosPy(path_repo_baixado)).strip() + "\n"

        if(desejaManterReposBaixados is not True):
            try:
                shutil.rmtree(path_repo_baixado, ignore_errors= True)
            except:
                print(r"O repositorio " + nome_repositorio + " não pode ser excluído!")

    print("\nTodos repositórios foram baixados com sucesso!")

    excluirPasta(repos_path)

    exportarLocsParaTXT(listaLocs, pathRelativaArquivoLocs)