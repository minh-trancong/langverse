# main_code.py

import warnings

import altair as alt
import cohere
import numpy as np
import pandas as pd
import pymongo
from annoy import AnnoyIndex
from searching.elassearch import get_results, get_search_key  # Import the results field from elas.py
# from sklearn.metrics.pairwise import cosine_similarity
# from tqdm import tqdm
# from transformers import AutoTokenizer, AutoModel
# from whoosh import scoring
# from whoosh.fields import Schema, TEXT
# from whoosh.index import create_in, open_dir
# from whoosh.qparser import QueryParser

warnings.filterwarnings('ignore')

# Set up Cohere API key
co = cohere.Client("GHkg6Kn1bJWB2G3MX0rHs29BqPPuM3m4fwfxKglr")
model_name = "embed-multilingual-v3.0"
api_key = ""
input_type_embed = "search_document"
search_key = get_search_key()

# Assume that the results are fetched from MongoDB, similar to your previous code
# You can replace this part with your actual MongoDB code
# Call the get_results function to get the actual results
results = get_results()

# Create a DataFrame from the results
df_results = pd.DataFrame(results)
# Concatenate text from all relevant columns into a single string
df_results['combined_text'] = df_results['config'].apply(lambda x: ' '.join(map(str, x))) + ' ' + df_results[
    'name'] + ' ' + df_results['price'].astype(str)

# Embed text using Cohere
embeds_combined = co.embed(texts=list(df_results['combined_text']), model=model_name,
                           input_type=input_type_embed).embeddings

# Create Annoy search index for the combined text
search_index_combined = AnnoyIndex(np.array(embeds_combined).shape[1], 'angular')
for i in range(len(embeds_combined)):
    search_index_combined.add_item(i, embeds_combined[i])
search_index_combined.build(10)  # 10 trees
search_index_combined.save('test_combined.ann')


# Function to get nearest neighbors for combined text
def get_nearest_neighbors_for_combined(query):
    input_type_query = "search_query"
    query_embed = co.embed(texts=[query], model=model_name, input_type=input_type_query).embeddings
    similar_item_ids = search_index_combined.get_nns_by_vector(query_embed[0], 5, include_distances=False)
    query_results = df_results.iloc[similar_item_ids].copy()
    return query_results


# Set Pandas options to display all columns
pd.set_option('display.max_columns', None)

# Example query
query = search_key
# Get nearest neighbors for combined text
combined_nearest_neighbors_result = get_nearest_neighbors_for_combined(query)

# Select only the 'name', 'price', and 'link' columns
global selected_fields
selected_fields = combined_nearest_neighbors_result[['name', 'price', 'link', 'config', 'promo']]

# Print the selected fields
print(selected_fields.to_string(index=False))


def get_selected_fields():
    return selected_fields