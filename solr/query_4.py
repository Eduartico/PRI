import requests
import json

SELECT_URL = 'http://localhost:8983/solr/movies/select'

# filmes de animação que tenham princesas 

'''
params = {
    'defType': 'edismax',
    'q': 'animation princess',
    'indent': 'true',
    'q.op': 'AND',
    'qf' : 'movie_title Keywords Overview',
    "fl" : "movie_title, Overview, Generes, Keywords",
    'bq': 'movie_title:princess movie_title:animation Keywords:animation Keywords:princess Overview:princess Overview:animation ',
    'wt': 'json',
}

'''

params = {
    'defType': 'edismax',
    'q': 'animation princess',
    'indent': 'true',
    'q.op': 'AND',
    'qf' : 'movie_title Keywords^2 Overview^3',
    "fl" : "movie_title, Overview, Generes, Keywords",
    'bq': 'movie_title:princess^2 movie_title:animation Keywords:animation^2 Keywords:princess^2 Overview:princess^3 Overview:animation^3 ',
    'wt': 'json',
}


# Faz a solicitação HTTP
response = requests.get(SELECT_URL, params=params)

# Obtém o JSON da resposta
result_json = response.json()

# Imprime a resposta com indentação
print(json.dumps(result_json, indent=2))



