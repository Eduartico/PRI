import requests
import json

SELECT_URL = 'http://localhost:8983/solr/movies/select'

# filmes de animação que tenham princesas dos anos 2000

params = {
    'q': 'Generes:(Animation) AND (Overview:princess OR Keywords:princess) AND year:[2000 TO 2009]',
    'indent': 'true',
    'fl': '*, [child]',
    'q.op': 'AND',
    'sort': 'Popularity desc',
    'wt': 'json',
}


# Faz a solicitação HTTP
response = requests.get(SELECT_URL, params=params)

# Obtém o JSON da resposta
result_json = response.json()

# Imprime a resposta com indentação
print(json.dumps(result_json, indent=2))



