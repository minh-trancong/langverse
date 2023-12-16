from elasticsearch import Elasticsearch
from pymongo import MongoClient
import json

# Connect to Elasticsearch
es = Elasticsearch('http://34.124.167.199:443')

# Connect to MongoDB
client = MongoClient('mongodb://34.124.167.199:80/')
db = client['chatbot']
collection = db['laptop']

# Iterate over all documents in the MongoDB collection
for document in collection.find():
    # Remove the MongoDB _id (it's not JSON serializable)
    document.pop('_id', None)

    # Index the document in Elasticsearch
    es.index(index='laptop', body=document)