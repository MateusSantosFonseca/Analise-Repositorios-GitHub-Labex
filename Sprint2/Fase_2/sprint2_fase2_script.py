import requests
import json
from csv import writer
import os
import os.path
import shutil

fase = r"\Fase_2"

def executar_query_github(query, headers):
    request = requests.post('https://api.github.com/graphql', json = {'query': query}, headers = headers)
    if request.status_code == 200:
        return request.json()
    elif request.status_code == 502:
        return executar_query_github(query, headers)
    else:
        raise Exception("A query falhou: {}. {}".format(request.status_code, query))

# Formatando as datas dos nodes para ficar mais limpo (yyyy-mm-dd)  
def formatar_datas(response):
    nodes = response['data']['search']['nodes']
    for i, repositorio in enumerate(nodes):
        nodes[i]['createdAt'] = nodes[i]['createdAt'].split("T")[0]
        
# Funcao responsavel por exportar o arquivo .csv final e por delegar a exportacao do arquivo .txt com as urls de clone dos repositorios
def exportar_arquivos(data):
    pathRelativa = os.getcwd() + fase + r"\output_repositorios_github.csv"
    listaURLS = ""
    with open(pathRelativa, 'w+') as csv_final:
        csvWriter = writer(csv_final)
        header = (["Nome", "Linguagem primária", "Quantidade de stars", "Watchers", "Data de criação", "Quantidade de forks", "URL"])
        csvWriter.writerow(header)
        for repo in data:
            repo = reposDictToString(repo)
            csvWriter.writerow(repo.values())
            listaURLS += repo['url'].strip() + "," + repo['name'] + "\n"
    exportarURLSparaTXT(listaURLS)

def exportarURLSparaTXT(listaURLS):
    pathRelativa = os.getcwd() + fase + r"\lista_urls_repos.txt"
    file = open(pathRelativa, "w+")  
    file.write(listaURLS)
    file.close

def reposDictToString(repo):

    if repo.get('name') is not None:
        repo['name'] = repo['name'] 

    if repo.get('createdAt') is not None:
        repo['createdAt'] = " " + repo['createdAt'] 
    
    if repo.get('stargazers') is not None:
        for key,val in repo.get('stargazers').items():
            repo['stargazers'] = " " + str(val)
    
    if repo.get('forks') is not None:
        for key,val in repo.get('forks').items():
            repo['forks'] = " " + str(val)

    if repo.get('primaryLanguage') is not None:        
        for key,val in repo.get('primaryLanguage').items():
            repo['primaryLanguage'] = " " + str(val)
    else:
        repo['primaryLanguage'] = " Linguagem não definida"

    if repo.get('watchers') is not None:        
        for key,val in repo.get('watchers').items():
            repo['watchers'] = " " + str(val)
    
    if repo.get('url') is not None:
        repo['url'] = " " + repo['url'] 

    return repo


def sprint2_fase2():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'bearer SEU_TOKEN_AQUI'
    }

    query = """
    {
        search(query:"language:Python stars:>100", type:REPOSITORY, first:10 {placeholder}){
            pageInfo {
                hasNextPage
                endCursor
            }
            nodes {
                ... on Repository {
                    name
                    primaryLanguage {
                        name
                    }
                    stargazers {
                        totalCount
                    }
                    watchers {
                        totalCount
                    }
                    createdAt
                    forks {
                        totalCount
                    }
                    url
                } 
            } 
        }
    }
    """

    # O placeholder é responsável por substituir o cursor da próxima pagina (na primeira iteração ele é descartado)
    query_inicial = query.replace("{placeholder}", "")

    # Rodando a primeira vez 
    response = executar_query_github(query_inicial, headers)
    quantidade_execucoes = 1 

    formatar_datas(response) 

    # Começa com um por já ter sido feita uma consulta
    cursor_final_atual = response["data"]["search"]["pageInfo"]["endCursor"] # Atualiza o cursor
    has_next_page = response["data"]["search"]["pageInfo"]["hasNextPage"] # Atualiza se tem proxima página
    todos_resultados = response["data"]["search"]["nodes"]

    # 10 paginas * 100 repositórios por pagina = 1000 repositorios.
    while (quantidade_execucoes < 100 and has_next_page):
        finalQuery = query.replace("{placeholder}", ', after: "%s"' % cursor_final_atual) # Troca a query para possuir o cursor
        
        response = executar_query_github(finalQuery, headers)
        
        formatar_datas(response)
        
        # Incrementa o output de resultados
        todos_resultados += response["data"]["search"]["nodes"]
        quantidade_execucoes += 1
    
        # Altera a proxima pagina
        has_next_page = response["data"]["search"]["pageInfo"]["hasNextPage"] 

        # Altera o cursor para o atual
        cursor_final_atual = response["data"]["search"]["pageInfo"]["endCursor"] 
    
    exportar_arquivos(todos_resultados)
