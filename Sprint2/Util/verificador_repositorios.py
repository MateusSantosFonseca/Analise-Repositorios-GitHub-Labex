import os

def exportarErrosLocParaTXT(pathRelativaArquivoErrosLocs, stringErrosLocs):
    file = open(pathRelativaArquivoErrosLocs, "w+")  
    file.write(stringErrosLocs)
    file.close

def runVerificadorErrosLocRepositoriosScriptMain(fase_atual):
    pathListaLocs = os.getcwd() + fase_atual + r"\lista_locs_repos.txt"
    pathUrlNomeRepos = os.getcwd() + fase_atual + r"\lista_urls_repos.txt"
    pathErrosLocs = os.getcwd() + fase_atual + r"\lista_repos_locs_com_erro.txt"

    try:
        with open(pathListaLocs, 'r') as file:
            locs_list = list(file)
    except:
        print("Ocorreu um problema na leitura dos arquivo de LOCS.")

    try:
        with open(pathUrlNomeRepos, 'r') as file:
            urls_nomes_list = list(file)
    except:
        print("Ocorreu um problema na leitura dos arquivo de urls e nomes de repositórios.")

    try:
        repositoriosComErro = "Repositórios com erro:\n\n"
        contadorRepos = -1
        contadorReposComErro = 0
        for loc in locs_list:
            contadorRepos += 1
            locAtual = loc.rstrip()
            if(locAtual == "0" or locAtual == "-1" or locAtual == "-2"):
                contadorReposComErro += 1
                repoAtual = urls_nomes_list[contadorRepos].split(',')[1].rstrip()
                repositoriosComErro += "O repositório: " + repoAtual + " apresentou erro na leitura de locs. Ele era o " + str(contadorRepos + 1) + "° repositório.\n\n"
        
        repositoriosComErro += "Houveram, ao todo, " + str(contadorReposComErro) + " repositórios com erro em seu download e, consequentemente, " + str(contadorReposComErro) + " LOCs não contados."
        exportarErrosLocParaTXT(pathErrosLocs, repositoriosComErro)
    except:
        print("Ocorreu um problema na verificação de LOCS com erro.")
