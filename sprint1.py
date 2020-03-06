import requests
import json
import csv

def executar_query_github(query):
    request = requests.post('https://api.github.com/graphql', json = {'query': query}, headers = headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("A query falhou: {}. {}".format(request.status_code, query))

def exportar_para_csv(data):
    outputFile = open("repositorios.csv", 'w+')
    for i, repositorio in enumerate(data):
        outputFile.write("\n" + json.dumps(data[i]) + "\n")

# Formatando as datas dos nodes para ficar mais limpo (yyyy-mm-dd)  
def formatar_datas(response):
    nodes = response['data']['search']['nodes']
    for i, repositorio in enumerate(nodes):
        nodes[i]['createdAt'] = nodes[i]['createdAt'].split("T")[0]
        nodes[i]['updatedAt'] = nodes[i]['updatedAt'].split("T")[0]

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'bearer 08a7e4d6ae0ddc541b76206a37549dad5f20a80a',
}

query = """
{
    search(query:"stars:>100", type:REPOSITORY, first:50 {placeholder}){
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
                pullRequests{ totalCount } 
                releases{ totalCount } 
                primaryLanguage{ name } 
                todasIssues: issues{ totalCount } 
                issuesFechadas: issues(states:CLOSED){ totalCount } 
            } 
        } 
    }
}
"""

# O placeholder é responsável por substituir o cursor da próxima pagina (na primeira iteração ele é descartado)
query_inicial = query.replace("{placeholder}", "")


# Rodando a primeira vez 
response = executar_query_github(query_inicial)
formatar_datas(response) 

# 20 paginas * 50 repositórios por pagina = 1000 repositorios. Começa com um por já ter sido feita uma consulta

quantidade_execucoes = 1 

cursor_final_atual = response["data"]["search"]["pageInfo"]["endCursor"] # Atualiza o cursor

has_next_page = response["data"]["search"]["pageInfo"]["hasNextPage"] # Atualiza se tem proxima página
todos_resultados = response["data"]["search"]["nodes"]


while (quantidade_execucoes < 20 and has_next_page):
    finalQuery = query.replace("{placeholder}", ', after: "%s"' % cursor_final_atual) # Troca a query para possuir o cursor
    
    response = executar_query_github(finalQuery) # Executa novamente a função que consome a API
    
    formatar_datas(response) # Formata as datas
    
    todos_resultados += response["data"]["search"]["nodes"] # Incrementa o output de resultados
    quantidade_execucoes += 1
   
     # Altera a proxima pagina
    has_next_page = response["data"]["search"]["pageInfo"]["hasNextPage"] 

    # Altera o cursor para o atual
    cursor_final_atual = response["data"]["search"]["pageInfo"]["endCursor"] 


exportar_para_csv(todos_resultados)