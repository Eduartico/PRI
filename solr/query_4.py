import requests
import json
import urllib.parse


SELECT_URL = 'http://localhost:8983/solr/movies/select'

# filmes de animação que tenham princesas 


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
'''


query_string = urllib.parse.urlencode(params)

# Combine the base URL and the query string
full_url = urllib.parse.urlunparse(('http', SELECT_URL, '', '', query_string, ''))

print(full_url)




