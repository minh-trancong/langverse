from elasticsearch import Elasticsearch

def test_connection(host):
    # Connect to Elasticsearch
    es = Elasticsearch(host)

    # Test connection
    if not es.ping():
        print(f"Can't connect to Elasticsearch at {host}")
    else:
        print(f"Successfully connected to Elasticsearch at {host}")

# Replace with your Elasticsearch host
host = 'http://34.124.167.199:443'
test_connection(host)