from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import requests
from sentence_transformers import SentenceTransformer
import json


solr_endpoint = "http://localhost:8983/solr"
collection = "movies"


def text_to_embedding(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(text, convert_to_tensor=False).tolist()
    
    # Convert the embedding to the expected format
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"
    return embedding_str

def solr_knn_query(endpoint, collection, embedding):
    url = f"{endpoint}/{collection}/select"

    data = {
        "q": f"{{!knn f=vector topK=10}}{embedding}",
        "fl": "movie_title,Overview,year,Rating,User_rating,Generes,Keywords,Director,Top_5_Casts,Writer,year,path,Popularity,Votes,Adult,Poster_Image,Taglines,Runtime,score",
        "rows": 10,
        "wt": "json"
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()

def display_results(results):
    docs = results.get("response", {}).get("docs", [])
    if not docs:
        return {"message": "No results found."}

    results_list = []
    for doc in docs:
        result_item = {
            "movie_title": doc.get('movie_title'),
            "Overview": doc.get('Overview'),
            "score": round(doc.get('score'), 2),
            "year": doc.get('year'),
            "Rating": doc.get('Rating'),
            "User_rating": doc.get('User_rating'),
            "Generes": doc.get('Generes'),
            "Keywords": doc.get('Keywords'),
            "Director": doc.get('Director'),
            "Top_5_Casts": doc.get('Top_5_Casts'),
            "Writer": doc.get('Writer'),
            "path": doc.get('path'),
            "Popularity": doc.get('Popularity'),
            "Votes": doc.get('Votes'),
            "Adult": doc.get('Adult'),
            "Poster_Image": doc.get('Poster_Image'),
            "Taglines": doc.get('Taglines'),
            "Runtime": doc.get('Runtime'),
        }
        results_list.append(result_item)

    return {"results": results_list}

@csrf_exempt
@require_POST
def search(request):
    try:
        print(request.body)
        data = json.loads(request.body.decode('utf-8'))
        query_text = data.get('query_text')
        embedding = text_to_embedding(query_text)
        results = solr_knn_query(solr_endpoint, collection, embedding)
        return JsonResponse(display_results(results), safe=False)
    except requests.HTTPError as e:
        return JsonResponse({"error": f"Error {e.response.status_code}: {e.response.text}"}, status=500)

