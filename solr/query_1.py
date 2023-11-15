import requests
import json

SELECT_URL = 'http://localhost:8983/solr/movies/select'

# filmes para vespera de natal

params = {
    'defType': 'edismax',
    'q': 'christmas eve',
    'indent': 'true',
    'q.op': 'AND',
    'qf' : 'movie_title Keywords Overview',
    "fl" : "movie_title, Overview, Generes, Keywords",
    'bq': 'movie_title:christmas Generes:Comedy Generes:Family Keywords:Christmas Keywords:christmas Overview: christmas ',
    'wt': 'json',
}
'''
params = {
    'defType': 'edismax',
    'q': 'christmas eve',
    'indent': 'true',
    'q.op': 'AND',
    'qf' : 'movie_title Keywords^3 Overview^2',
    "fl" : "movie_title, Overview, Generes, Keywords",
    'bq': 'movie_title:christmas^2 Generes:Comedy Generes:Family Keywords:Christmas^2 Keywords:christmas^3 Overview: christmas^2 ',
    'wt': 'json',
}
'''
# Faz a solicitação HTTP
response = requests.get(SELECT_URL, params=params)

# Obtém o JSON da resposta
result_json = response.json()


# Imprime a resposta com indentação
print(json.dumps(result_json, indent=2))

