import cohere
import os
import json
import numpy as np
from sklearn.neighbors import NearestNeighbors

# Initialize the Cohere client
co = cohere.Client('ZdmchLQ5VOe6SOLqVR5JJcqOGCyq2KzBWC4f6bOK')

# Define the directory
directory = '../crawler/tgdd'

# Get a list of all json files in the directory
json_files = [f for f in os.listdir(directory) if f.endswith('.json')]

# Initialize an empty list to store the embeddings
list_embeddings = []
file_info = []

# For each file
for file in json_files:
    # Open the file
    with open(os.path.join(directory, file), 'r') as f:
        # Load the json data
        data = json.load(f)
        
        # Assume each json file contains a sentence under the 'sentence' key
        # Generate embeddings for the sentence
        response = co.embed(
            texts=[data['sentence']],
            model='embed-multilingual-v3.0',
            input_type='search_document'
        )

        # The embeddings are stored in 'embeddings' field of the response
        embedding = response.embeddings[0]

        # Append the embedding to the 'list_embeddings' list
        list_embeddings.append(embedding)
        file_info.append(file)

# Convert list_embeddings to a numpy array
list_embeddings = np.array(list_embeddings)

# Create a NearestNeighbors model
model = NearestNeighbors(n_neighbors=5)  # Replace 5 with the number of neighbors you want
model.fit(list_embeddings)

# Assume 'user_sentence' is the sentence from the user input
user_sentence = '...'  # Replace with your actual user sentence

# Generate embedding for the user sentence
response = co.embed(
    texts=[user_sentence],
    model='embed-multilingual-v3.0',
    input_type='search_document'
)

# The embedding is stored in 'embeddings' field of the response
user_embedding = response.embeddings[0]

# Find the top k nearest neighbors to the user_embedding
distances, indices = model.kneighbors([user_embedding])

# Get the file info for the top k nearest neighbors
top_k_files = [file_info[i] for i in indices[0]]

# Now 'top_k_files' contains the file info for the top k nearest neighbors
print(top_k_files)