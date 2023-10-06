import pandas as pd
import requests
def exclude_columns(input_path, columns_to_exclude, output_path):
    df = pd.read_csv(input_path)
    df = df.drop(columns=columns_to_exclude)
    df.to_csv(output_path, index=False)
    print(f"Columns {', '.join(columns_to_exclude)} removed and new file saved as '{output_path}'" + '\n')

def merge_columns(df1, df2, column_A, column_B):
    # Copy the first DataFrame to a new one
    merged_df = df1.copy()
    # Merge the two specified columns and remove duplicate words
    merged_df[column_A] = merged_df[column_A].str.lower().str.split()
    df2[column_B] = df2[column_B].str.lower().str.split()
    merged_df[column_A] = merged_df.apply(lambda row: " ".join(set(row[column_A] + df2[df2.index == row.name][column_B].values[0])), axis=1)

    return merged_df

def get_movie_details(api_key, movie_id):
    # Define the base URL for movie details API
    base_url = "https://api.themoviedb.org/3/movie/"

    # Construct the full URL with the provided movie ID
    url = f"{base_url}{movie_id}?language=en-US"

    # Set up headers with your API key
    headers = {
        "accept": "application/json",
        "Authorization": f"{api_key}"
    }
    # Make the API request
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Return the JSON response
        return response.json()
    else:
        # Print API request error and return None
        print(f"Error fetching movie details for movie ID {movie_id}. Status code: {response.status_code}")
        return None

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
runtimes = []
taglines = []

# Define your API key and base URL
api_key = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzM2NmRkMTljN2M0NzBkNDc0NTIwZDk2NjBiNDc0MiIsInN1YiI6IjY1MWZjM2E0M2QzNTU3MDExYzAwZDM4NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.GbPjzum6QyDvy2MZY-3vqr1TkeFg7lgoCqdudQwTfQU"
base_url = "https://api.themoviedb.org/3/search/movie"
movie_count = 1

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
        movie_id = result.get('id', None)

        details = get_movie_details(api_key, movie_id)

        if details.get('status', None) != 'Released':
            break

        popularity_score = details.get('popularity', None)
        vote_count = details.get('vote_count', None)
        release_date = details.get('release_date', None)
        adult_flag = details.get('adult', None)
        poster_path = details.get('poster_path', None)
        runtime = details.get('runtime', None)
        tagline = details.get('tagline', None)

        # Append the data to the respective lists
        popularity.append(popularity_score)
        votes.append(vote_count)
        release_dates.append(release_date)
        adult.append(adult_flag)
        poster_images.append("http://image.tmdb.org/t/p/w500" + poster_path)
        runtimes.append(runtime)
        taglines.append(tagline)
        print(
            "Added this release date: " + str(votes[-1]) + " " + str(popularity[-1]) + " " + str(adult[-1]) + " " + str(
                poster_images[-1]) + " to movie " + movie_title)
        movie_count += 1
        if movie_count % 1000 == 0:
            data['Popularity'] = popularity
            data['Votes'] = votes
            data['Release Date'] = release_dates
            data['Adult'] = adult
            data['Poster Image'] = poster_images
            data['Runtime'] = runtimes
            data['Taglines'] = taglines

            # Save the updated DataFrame to a new CSV file
            data.to_csv('updated_data.csv', index=False)

    else:
        # Print API request error and movie title for debugging
        print(f"Error fetching data for {movie_title}. Status code: {response.status_code}")

# Add the extracted data to the DataFrame
data['Popularity'] = popularity
data['Votes'] = votes
data['Release Date'] = release_dates
data['Adult'] = adult
data['Poster Image'] = poster_images
data['Runtime'] = runtimes
data['Taglines'] = taglines

# Save the updated DataFrame to a new CSV file
data.to_csv('updated_data.csv', index=False)