import requests
import json
import urllib.parse

SELECT_URL = 'http://localhost:8983/solr/movies/select'

# filmes para vespera de natal
'''
params = {
    'defType': 'edismax',
    'q': 'christmas eve',
    'indent': 'true',
    'q.op': 'AND',
    'qf' : 'movie_title Keywords Overview Generes',
    "fl" : "movie_title, Overview, Generes, Keywords",
    'wt': 'json',
    'rows': 20
}
'''
params = {
    'defType': 'edismax',
    'q': 'christmas eve',
    'indent': 'true',
    'q.op': 'AND',
    'qf' : 'movie_title Keywords^10 Overview^5 Generes' ,
    "fl" : "movie_title, Overview, Generes, Keywords",
    'wt': 'json',
    'rows': 20

}


query_string = urllib.parse.urlencode(params)

# Combine the base URL and the query string
full_url = urllib.parse.urlunparse(('http', SELECT_URL, '', '', query_string, ''))

#print(full_url)
# Faz a solicitação HTTP
response = requests.get(SELECT_URL, params=params)

# Obtém o JSON da resposta
result_json = response.json()


# Imprime a resposta com indentação
print(json.dumps(result_json, indent=2))

