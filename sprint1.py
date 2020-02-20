import requests
import json

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'bearer 08a7e4d6ae0ddc541b76206a37549dad5f20a80a',
}

data = '{"query": "{ search(query:\\"stars:>100\\", type:REPOSITORY, first:100){ nodes { ... on Repository {nameWithOwner url createdAt updatedAt pullRequests{ totalCount } releases{ totalCount } primaryLanguage{ name } todasIssues: issues{ totalCount } issuesFechadas: issues(states:CLOSED){ totalCount } } } } }"}'

response = requests.post(
	'https://api.github.com/graphql', headers=headers, data=data)


json_data = json.loads(response.text)

nodes = json_data['data']['search']['nodes']

# Formatando as datas dos nodes para ficar mais limpo (yyyy-mm-dd)
for i, repositorio in enumerate(nodes):
    nodes[i]['createdAt'] = nodes[i]['createdAt'].split("T")[0]
    nodes[i]['updatedAt'] = nodes[i]['updatedAt'].split("T")[0]
    # print("\n", nodes[i]) # Printando apenas os nodes

print (json_data)