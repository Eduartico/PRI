import sys
import json
from sentence_transformers import SentenceTransformer

# Load the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    # The model.encode() method already returns a list of floats
    return model.encode(text, convert_to_tensor=False).tolist()

if __name__ == "__main__":
    # Read JSON from STDIN
    data = json.load(sys.stdin)

    # Update each document in the JSON data
    for document in data:
        # Extract fields if they exist, otherwise default to empty strings
        # Extract fields if they exist, otherwise default to empty strings
        Overview = document.get("Overview", "")
        title = document.get("movie title", "")
        year = document.get("year", "")
        director = document.get("Director", "")
        writer = document.get("Writer", "")
        genres = document.get("Generes", "")
        keywords = document.get("Keywords", "")
        # Convert genres list to string
        genres_str = ", ".join(genres)
        keywords_str = ", ".join(keywords)
        
        combined_text = title + " " + Overview + " " + str(year) + " " + director + " " + writer + " " + genres_str + " " + keywords_str
        document["vector"] = get_embedding(combined_text)

    # Output updated JSON to STDOUT
    json.dump(data, sys.stdout, indent=4, ensure_ascii=False)
