import requests
import json

SELECT_URL = 'http://localhost:8983/solr/movies/select'

# filmes com tematica de romance na adolescencia do diretor John Hughes ou Greta Gerwig
params = {
    'q': 'Generes:(Romance) AND (Overview:(adolescence OR teen) OR Keywords:(adolescence OR teen))',
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

