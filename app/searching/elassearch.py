from elasticsearch import Elasticsearch
from pymongo import MongoClient
import json
# from keysearch import keysearch

# Connect to Elasticsearch
es = Elasticsearch('http://34.124.167.199:443')

# Connect to MongoDB
client = MongoClient('mongodb://34.124.167.199:80/')
db = client['chatbot']
collection = db['laptop']

# Get the search key
# search_key = keysearch()

# Perform the search
response = es.search(
    index="laptop",
    body={
        "query": {
            "match": {
                "config": "bộ nhớ 512GB"            
            }
        }
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

# Print the results
for i, result in enumerate(results, 1):
    print(f"Result {i}: {result}")