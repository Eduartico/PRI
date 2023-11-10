import pandas as pd
import ast
import json

# Lê o arquivo JSON para um DataFrame
# Substitua 'seu_arquivo.json' pelo caminho real do seu arquivo JSON
data = pd.read_json('solr/final_data.json')

# Função para converter strings de listas para listas reais
def convert_string_to_list(string):
    try:
        return ast.literal_eval(string)
    except (SyntaxError, ValueError):
        # Se houver algum erro ao avaliar a string como uma lista, retorna a string original
        return string

# Aplica a função à coluna "Generes"
data["Generes"] = data["Generes"].apply(convert_string_to_list)
data["Keywords"] = data["Keywords"].apply(convert_string_to_list)
data["Top 5 Casts"] = data["Top 5 Casts"].apply(convert_string_to_list)

# Salva o DataFrame atualizado em um novo arquivo JSON
data.to_json('updated_data.json', orient='records')