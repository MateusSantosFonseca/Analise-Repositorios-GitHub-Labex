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
    for i, repositorio in enumerate(nodes):
        outputFile.write("\n" + json.dumps(nodes[i]) + "\n")


headers = {
    'Content-Type': 'application/json',
    'Authorization': 'bearer 08a7e4d6ae0ddc541b76206a37549dad5f20a80a',
}

data = """
{
    search(query:"stars:>100", type:REPOSITORY, first:100){
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

response = executar_query_github(data)

nodes = response['data']['search']['nodes']

# Formatando as datas dos nodes para ficar mais limpo (yyyy-mm-dd)
for i, repositorio in enumerate(nodes):
    nodes[i]['createdAt'] = nodes[i]['createdAt'].split("T")[0]
    nodes[i]['updatedAt'] = nodes[i]['updatedAt'].split("T")[0]
    # print("\n", nodes[i]) # Printando apenas os nodes

exportar_para_csv(response)