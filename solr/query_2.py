import requests
import json

SELECT_URL = 'http://localhost:8983/solr/movies/select'

# filmes com tematica de romance na adolescencia
'''
params = {
    'defType': 'edismax',
    'q': 'teen romance',
    'indent': 'true',
    'q.op': 'AND',
    'qf' : 'movie_title Keywords Overview Generes',
    "fl" : "movie_title, Overview, Generes, Keywords",
    'wt': 'json',
}
'''
params = {
    'defType': 'edismax',
    'q': 'teen romance',
    'indent': 'true',
    'q.op': 'AND',
    'qf' : 'movie_title Keywords^10 Overview^5 Generes',
    "fl" : "movie_title, Overview, Generes, Keywords",
    'wt': 'json',
}





# Faz a solicitação HTTP
response = requests.get(SELECT_URL, params=params)

# Obtém o JSON da resposta
result_json = response.json()

# Imprime a resposta com indentação
print(json.dumps(result_json, indent=2))

