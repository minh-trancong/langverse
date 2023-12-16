import cohere
from pymongo import MongoClient

# Initialize the Cohere client
co = cohere.Client('24RfnVBtZyRFukqs02fyOHL8xF87JKHO1dzd9qcz')

# GHkg6Kn1bJWB2G3MX0rHs29BqPPuM3m4fwfxKglr
# 24RfnVBtZyRFukqs02fyOHL8xF87JKHO1dzd9qcz
# ZdmchLQ5VOe6SOLqVR5JJcqOGCyq2KzBWC4f6bOK

# Connect to MongoDB
client = MongoClient('mongodb://34.124.167.199:80/')
db = client['chatbot']  # Replace with your actual database
collection = db['laptop']  # Replace with your actual collection

# Get documents from 11th to 20th from the collection
documents = collection.find().skip(95).limit(10)

# For each document
for document in documents:
    # Combine all fields in the document into a single string
    text = ' '.join(str(value) for value in document.values())

    # Use Cohere to summarize the text
    response = co.summarize(text=text, format='bullets', temperature=0, length='long', model='command-light')

    # Add the summary to the document
    document['summary'] = response.summary

    # Update the document in MongoDB
    collection.update_one({'_id': document['_id']}, {'$set': document})