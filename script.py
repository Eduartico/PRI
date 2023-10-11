
from time import sleep
import pandas as pd
import requests
import ast
import re
import numpy as np
import os


data = pd.read_csv('final_data.csv')

data['year'] = pd.to_numeric(data['year'], errors='coerce')

data = data.dropna(subset=['year'])

#data['year'] = data['year'].abs()

data = data[data['year'].apply(lambda x: x == int(x))]


for value in data['year']:
    print(f'Tipo da entrada: {type(value)}')

data.to_csv('final_data2.csv', index=False)