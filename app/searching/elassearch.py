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

# Define the search key as a global variable
global search_key
search_key = keysearch()

# Define a getter function for the search key
def get_search_key():
    return search_key

# Perform the search
response = es.search(
    index="laptop",
    body={
        "query": {
            "match": {
                "config": search_key
            }
        }, "size":30
    }
)

# Get all results
all_results = response['hits']['hits']

# Get the number of results
num_results = len(all_results)

# Print the number of results
print(f"Number of results: {num_results}")

# Extract the 'link' field from each result
global results
results = [result['_source'] for result in all_results]

def get_results():
    return results

# Print the results
# for i, result in enumerate(results, 1):
#     print(f"Result {i}: {result}")