import requests
import json
from csv import writer

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
    nodes = response['data']['search']['nodes']
    for i, repositorio in enumerate(nodes):
        nodes[i]['createdAt'] = nodes[i]['createdAt'].split("T")[0]
        nodes[i]['updatedAt'] = nodes[i]['updatedAt'].split("T")[0]
        
def exportar_para_csv(data):
    with open("output_repositorios_github.csv", 'w+') as csv_final:
        csvWriter = writer(csv_final)
        header = (["Nome", "URL", "Criado em", "Atualizado em", "Quantidade de stars", "Pull Requests aceitas", "Pull Requests totais", "Releases", "Linguagem primária", "Todas Issues", "Issues fechadas"])
        csvWriter.writerow(header)
        for repo in data:
            repo = reposDictToString(repo)
            csvWriter.writerow(repo.values())

# Alguns valores do repositorio vem no formato dict, isto atrapalha a formatacao do .csv, para não atrapalhar, 
# esta funcao converte os dicts da query em string. Além disso, aproveitando a funcao, acrescenta um espaco após cada virgula.
# Esta funcao necessita de refatoração

def reposDictToString(repo):

    if repo.get('nameWithOwner') is not None:
        repo['nameWithOwner'] = repo['nameWithOwner'] 

    if repo.get('url') is not None:
        repo['url'] = " " + repo['url'] 

    if repo.get('createdAt') is not None:
        repo['createdAt'] = " " + repo['createdAt'] 

    if repo.get('updatedAt') is not None:
        repo['updatedAt'] = " " + repo['updatedAt'] 

    if repo.get('pullRequestsAceitas') is not None:
        for key,val in repo.get('pullRequestsAceitas').items():
            repo['pullRequestsAceitas'] = " " + str(val)
    
    if repo.get('stargazers') is not None:
        for key,val in repo.get('stargazers').items():
            repo['stargazers'] = " " + str(val)
    
    if repo.get('pullRequests') is not None:
        for key,val in repo.get('pullRequests').items():
            repo['pullRequests'] = " " + str(val)

    if repo.get('releases') is not None:       
        for key,val in repo.get('releases').items():
            repo['releases'] = " " + str(val)

    if repo.get('primaryLanguage') is not None:        
        for key,val in repo.get('primaryLanguage').items():
            repo['primaryLanguage'] = " " + str(val)
    else:
        repo['primaryLanguage'] = " Linguagem não definida"

    if repo.get('todasIssues') is not None:        
        for key,val in repo.get('todasIssues').items():
            repo['todasIssues'] = " " + str(val)

    if repo.get('issuesFechadas') is not None:        
        for key,val in repo.get('issuesFechadas').items():
            repo['issuesFechadas'] = " " + str(val)        
    
    return repo


headers = {
    'Content-Type': 'application/json',
    'Authorization': 'bearer SEU_TOKEN_AQUI'
}

query = """
{
    search(query:"stars:>100", type:REPOSITORY, first:10 {placeholder}){
        pageInfo {
            hasNextPage
            endCursor
        }
        nodes {
        ... on Repository {
                nameWithOwner
                url
                createdAt 
                updatedAt
                stargazers { totalCount }
                pullRequestsAceitas: pullRequests(states: MERGED){ totalCount } 
                pullRequests{ totalCount } 
                releases{ totalCount } 
                primaryLanguage{ name } 
                todasIssues: issues{ totalCount } 
                issuesFechadas: issues(states: CLOSED){ totalCount } 
            } 
        } 
    }
}
"""

# O placeholder é responsável por substituir o cursor da próxima pagina (na primeira iteração ele é descartado)
query_inicial = query.replace("{placeholder}", "")

# Rodando a primeira vez 
response = executar_query_github(query_inicial)
quantidade_execucoes = 1 

formatar_datas(response) 

# Começa com um por já ter sido feita uma consulta
cursor_final_atual = response["data"]["search"]["pageInfo"]["endCursor"] # Atualiza o cursor
has_next_page = response["data"]["search"]["pageInfo"]["hasNextPage"] # Atualiza se tem proxima página
todos_resultados = response["data"]["search"]["nodes"]

# 20 paginas * 50 repositórios por pagina = 1000 repositorios.
while (quantidade_execucoes < 100 and has_next_page):
    finalQuery = query.replace("{placeholder}", ', after: "%s"' % cursor_final_atual) # Troca a query para possuir o cursor
    
    response = executar_query_github(finalQuery)
    
    formatar_datas(response)
    
    # Incrementa o output de resultados
    todos_resultados += response["data"]["search"]["nodes"] 
    quantidade_execucoes += 1
   
     # Altera a proxima pagina
    has_next_page = response["data"]["search"]["pageInfo"]["hasNextPage"] 

    # Altera o cursor para o atual
    cursor_final_atual = response["data"]["search"]["pageInfo"]["endCursor"] 

exportar_para_csv(todos_resultados)