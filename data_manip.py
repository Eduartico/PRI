import pandas as pd
import requests
def exclude_columns(input_path, columns_to_exclude, output_path):
    df = pd.read_csv(input_path)
    df = df.drop(columns=columns_to_exclude)
    df.to_csv(output_path, index=False)
    print(f"Columns {', '.join(columns_to_exclude)} removed and new file saved as '{output_path}'" + '\n')

# EDIT RAW
input_path = 'original_data.csv'
columns_to_exclude = ['Run Time', 'Rating', 'User Rating', 'year']
output_path = 'modified_data.csv'

exclude_columns(input_path, columns_to_exclude, output_path)

# Load your modified_data.csv file into a Pandas DataFrame
data = pd.read_csv('modified_data.csv')

# Initialize empty lists to store the extracted data
popularity = []
votes = []
release_dates = []
adult = []
poster_images = []

# Define your API key and base URL
api_key = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzM2NmRkMTljN2M0NzBkNDc0NTIwZDk2NjBiNDc0MiIsInN1YiI6IjY1MWZjM2E0M2QzNTU3MDExYzAwZDM4NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.GbPjzum6QyDvy2MZY-3vqr1TkeFg7lgoCqdudQwTfQU"
base_url = "https://api.themoviedb.org/3/search/movie"

# Iterate through each movie title in the DataFrame
for movie_title in data['movie title']:
    # Prepare the API request URL by replacing "name_stub" with the movie title
    url = base_url + f"?query={movie_title}&include_adult=true&page=1"

    # Set up headers with your API key
    headers = {
        "accept": "application/json",
        "Authorization": f"{api_key}"
    }

    # Make the API request
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        result = response.json()['results'][0]  # Take the first result

        # Extract the desired data
        popularity_score = result.get('popularity', None)
        vote_count = result.get('vote_count', None)
        release_date = result.get('release_date', None)
        adult_flag = result.get('adult', None)
        poster_path = result.get('poster_path', None)

        # Append the data to the respective lists
        popularity.append(popularity_score)
        votes.append(vote_count)
        release_dates.append(release_date)
        adult.append(adult_flag)
        poster_images.append(poster_path)
        print(
            "Added this release date: " + str(votes[-1]) + " " + str(popularity[-1]) + " " + str(adult[-1]) + " " + str(
                poster_images[-1]) + " to movie " + movie_title)
    else:
        # Print API request error and movie title for debugging
        print(f"Error fetching data for {movie_title}. Status code: {response.status_code}")

# Add the extracted data to the DataFrame
data['Popularity'] = popularity
data['Votes'] = votes
data['Release Date'] = release_dates
data['Adult'] = adult
data['Poster Image'] = poster_images

# Save the updated DataFrame to a new CSV file
data.to_csv('updated_data.csv', index=False)





