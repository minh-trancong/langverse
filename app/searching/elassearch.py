from elasticsearch import Elasticsearch
from pymongo import MongoClient
import json
from searching.keysearch import keysearch

# Connect to Elasticsearch
es = Elasticsearch('http://34.124.167.199:443')

# Connect to MongoDB
client = MongoClient('mongodb://34.124.167.199:80/')
db = client['chatbot']
collection = db['laptop']

# Define a getter function for the search key
def get_search_key():
    search_key = keysearch()
    return search_key

def perform_search():
    # Perform the search
    response = es.search(
        index="laptop",
        body={
            "query": {
                "match": {
                    "config": get_search_key()
                }
            }, "size":5
        }
    )

    # Get all results
    all_results = response['hits']['hits']

    # Get the number of results
    num_results = len(all_results)

    # Print the number of results
    print(f"Number of results: {num_results}")

    # Extract the 'link' field from each result
    results = [result['_source']['link'] for result in all_results]

    return results

def get_results():
    results = perform_search()
    return results