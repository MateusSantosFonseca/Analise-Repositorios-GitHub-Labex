import requests
import json
from csv import writer
import os
import os.path
import shutil


def executar_query_github(query):
    request = requests.post('https://api.github.com/graphql', json = {'query': query}, headers = headers)
    if request.status_code == 200:
        return request.json()
    elif request.status_code == 502:
        return executar_query_github(query)
    else:
        raise Exception("A query falhou: {}. {}".format(request.status_code, query))

# Formatando as datas dos nodes para ficar mais limpo (yyyy-mm-dd)  
def formatar_datas(response):
    nodes = response['data']['user']['repositories']['nodes']
    for i, repositorio in enumerate(nodes):
        nodes[i]['createdAt'] = nodes[i]['createdAt'].split("T")[0]
        
# Funcao responsavel por exportar o arquivo .csv final e por delegar a exportacao do arquivo .txt com as urls de clone dos repositorios
def exportar_arquivos(data):
    pathRelativa = os.getcwd() + "\output_repositorios_github.csv"
    listaURLS = ""
    with open(pathRelativa, 'w+') as csv_final:
        csvWriter = writer(csv_final)
        header = (["Nome", "Linguagem primária", "Quantidade de stars", "Watchers", "Data de criação", "Quantidade de forks", "URL"])
        csvWriter.writerow(header)
        repositorios = data['data']['user']['repositories']['nodes']
        for repo in repositorios:
            repo = reposDictToString(repo)
            if repo['primaryLanguage'] == " Python":
                csvWriter.writerow(repo.values())
                listaURLS += repo['url'].strip() + "," + repo['name'] + "\n"
    exportarURLSparaTXT(listaURLS)

def exportarURLSparaTXT(listaURLS):
    pathRelativa = os.getcwd() + "\lista_urls_repos.txt"
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


headers = {
    'Content-Type': 'application/json',
    'Authorization': 'bearer SEU_TOKEN_AQUI'
}

# Conferir se em repositories deve possuir isFork = false
query = """
{
  user(login: "gvanrossum") {
    repositories(first: 50) {
      nodes {
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

# Necessita de push access
# collaborators {
#         totalCount
#       }

response = executar_query_github(query)

formatar_datas(response) 

exportar_arquivos(response)