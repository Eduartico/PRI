from time import sleep
import pandas as pd
import requests
import ast
import re
import numpy as np
def exclude_columns(input_path, columns_to_exclude, output_path):
    df = pd.read_csv(input_path)
    df = df.drop(columns=columns_to_exclude)
    df.to_csv(output_path, index=False)
    print(f"Columns {', '.join(columns_to_exclude)} removed and new file saved as '{output_path}'" + '\n')

def get_movie_details(api_key, movie_id):
    base_url = "https://api.themoviedb.org/3/movie/"
    url = f"{base_url}{movie_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"{api_key}"
    }
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Return the JSON response
        return response.json()
    else:
        # Print API request error and return None
        print(f"Error fetching movie details for movie ID {movie_id}. Status code: {response.status_code}")
        return None

def get_movie_keywords(api_key, movie_id):
    base_url = "https://api.themoviedb.org/3/movie/"
    url = f"{base_url}{movie_id}/keywords" # Use string formatting here
    headers = {
        "accept": "application/json",
        "Authorization": f"{api_key}"
    }
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Return the JSON response
        #print(response.json())
        return response.json()
    else:
        # Print API request error and return None
        print(f"Error fetching movie details for movie ID {movie_id}. Status code: {response.status_code}")
        return None

def has_non_numeric(title):
    return bool(re.search(r'[^\d]', title))


# EDIT RAW
input_path = 'original_data.csv'
columns_to_exclude = ['Run Time', 'Rating', 'User Rating', 'year']
output_path = 'modified_data.csv'

exclude_columns(input_path, columns_to_exclude, output_path)

data = pd.read_csv('original_data.csv')
mask = data['movie title'].apply(has_non_numeric)
data = data[mask]
data.drop_duplicates(subset='movie title', inplace=True)


popularity = []
votes = []
release_dates = []
adult = []
poster_images = []
runtimes = []
taglines = []
new_keywords = []
movie_keywords = []

# Define API key and base URL
api_key = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzM2NmRkMTljN2M0NzBkNDc0NTIwZDk2NjBiNDc0MiIsInN1YiI6IjY1MWZjM2E0M2QzNTU3MDExYzAwZDM4NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.GbPjzum6QyDvy2MZY-3vqr1TkeFg7lgoCqdudQwTfQU"
base_url = "https://api.themoviedb.org/3/search/movie"
movie_count = 1

# Iterate through each movie title in the DataFrame
for movie_title in data['movie title']:
    url = base_url + f"?query={movie_title}&include_adult=true&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"{api_key}"
    }
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        results = response.json().get('results', [])  # Get the 'results' list or an empty list if not found

        if results:
            result = results[0]  # Take the first result
            # Extract the desired data
            movie_id = result.get('id', None)

            details = get_movie_details(api_key, movie_id)
            keyword = get_movie_keywords(api_key, movie_id)


            popularity_score = details.get('popularity', np.nan)
            vote_count = details.get('vote_count', np.nan)
            release_date = details.get('release_date', np.nan)
            adult_flag = details.get('adult', np.nan)
            poster_path = details.get('poster_path', None)
            runtime = details.get('runtime', np.nan)
            tagline = details.get('tagline', np.nan)
            keywords = keyword.get("keywords", [])

            # Append the data to the respective lists

            popularity.append(popularity_score)
            votes.append(vote_count)
            release_dates.append(release_date)
            adult.append(adult_flag)

            if poster_path is None:
                poster_images.append(np.nan)
            else:
                poster_images.append("http://image.tmdb.org/t/p/w500" + poster_path)

            runtimes.append(runtime)
            taglines.append(tagline)
            keyword_names = []
            for keyword in keywords:
                keyword_names.append(keyword['name'])
        
            # Append the movie's keywords to the movie_keywords list
            #print(type(keyword_names))
            if keyword_names is None:
                movie_keywords.append([])
            else:
                movie_keywords.append(keyword_names)

            sleep(0.015)
            #print(
                #"Added this release date: " + str(votes[-1]) + " " + str(popularity[-1]) + " " + str(adult[-1]) + " " + str(
                    #poster_images[-1]) + " to movie " + movie_title)
        else:
            # Handle the case when no results are found for the movie title
            popularity.append(np.nan)
            votes.append(np.nan)
            release_dates.append(np.nan)
            adult.append(np.nan)
            poster_images.append(np.nan)
            runtimes.append(np.nan)
            taglines.append(np.nan)
            movie_keywords.append(np.nan)

            print(f"No results found for {movie_title}")
        print(len(movie_keywords))
    else:
        # Print API request error and movie title for debugging
        print(f"Error fetching data for {movie_title}. Status code: {response.status_code}")

# Add the extracted data to the DataFrame
data['Popularity'] = popularity
data['Votes'] = votes
data['Adult'] = adult
data['Poster Image'] = poster_images
data['Runtime'] = runtimes
data['Taglines'] = taglines

aux_list = []

lista1 = [ast.literal_eval(item) for item in data['Keywords'].tolist()]

aux_list = []

for sublista1, sublista2 in zip(lista1, movie_keywords):      
    # Verifique se ambas as sublistas não estão vazias antes de concatená-las
    if isinstance(sublista1, list) and isinstance(sublista2, list):
        aux_list.append(sublista1 + sublista2)      
    elif isinstance(sublista1, list):
        aux_list.append(sublista1)
    elif isinstance(sublista2, list):    
        aux_list.append(sublista2)
    else:
        aux_list.append([])
    

data['Keywords'] = aux_list

# Remove all table entries with a null column
columns = ['Popularity', 'Votes', 'Adult', 'Poster Image', 'Runtime', 'Taglines']
data = data.dropna(axis=0, subset=columns)

# Save the updated DataFrame to a new CSV file
data.to_csv('updated_data.csv', index=False)