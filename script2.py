import pandas as pd
import ast
import json

# Lê o arquivo JSON para um DataFrame
# Substitua 'seu_arquivo.json' pelo caminho real do seu arquivo JSON
data = pd.read_json('solr/final_data.json')

data = data[data['Rating'] != 'no-rating']

data.to_json('final_data2.json', orient='records')



