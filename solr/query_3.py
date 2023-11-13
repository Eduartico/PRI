import requests
import json

SELECT_URL = 'http://localhost:8983/solr/movies/select'

# filmes de terror que não são sobrenaturais dos diretores Wes Craven ou John Carpenter
# Aqui está a resultados mal, por exemplo está a aparecer diretores com o nome John mas o apelido n é Carpenter
params = {
    'q': 'Generes:Horror AND NOT Generes:(Supernatural OR Paranormal) AND Director:(Wes Craven OR John Carpenter)',
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

