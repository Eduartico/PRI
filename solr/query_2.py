import requests
import json

SELECT_URL = 'http://localhost:8983/solr/movies/select'

# filmes com tematica de romance na adolescencia

params = {
    'defType': 'edismax',
    'q': 'teen romance',
    'indent': 'true',
    'q.op': 'AND',
    'qf' : 'movie_title Keywords Overview',
    "fl" : "movie_title, Overview, Generes, Keywords",
    'bq': 'movie_title:romance Generes:Romance Keywords:teen Keywords:romance Overview:teen Overview:romance ',
    'wt': 'json',
}
'''
params = {
    'defType': 'edismax',
    'q': 'teen romance',
    'indent': 'true',
    'q.op': 'AND',
    'qf' : 'movie_title Keywords^2 Overview^3',
    "fl" : "movie_title, Overview, Generes, Keywords",
    'bq': 'movie_title:romance^2 Generes:Romance^3 Keywords:teen^2 Keywords:romance^2 Overview:teen^2 Overview:romance^2 ',
    'wt': 'json',
}
'''




# Faz a solicitação HTTP
response = requests.get(SELECT_URL, params=params)

# Obtém o JSON da resposta
result_json = response.json()

# Imprime a resposta com indentação
print(json.dumps(result_json, indent=2))

