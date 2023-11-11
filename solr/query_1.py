import requests
import json

SELECT_URL = 'http://localhost:8983/solr/movies/select'

# filmes para vespera de natal
params = {
    'q': '(Generes:(Christmas OR Comedy OR Family) AND Keywords: Christmas) AND NOT Generes:Horror OR Overview:(holiday OR heartwarming)',
    'indent': 'true',
    'fl': '*, [child]',
    'q.op': 'OR',
    'sort': 'Popularity desc',
    'wt': 'json',
}


# Faz a solicitação HTTP
response = requests.get(SELECT_URL, params=params)

# Obtém o JSON da resposta
result_json = response.json()

# Imprime a resposta com indentação
print(json.dumps(result_json, indent=2))

