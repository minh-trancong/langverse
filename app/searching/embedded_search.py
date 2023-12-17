# embedded_search.py

import warnings

import altair as alt
import cohere
import numpy as np
import pandas as pd
import pymongo
from annoy import AnnoyIndex
from searching.elassearch import get_results, get_search_key

warnings.filterwarnings('ignore')

co = cohere.Client("GHkg6Kn1bJWB2G3MX0rHs29BqPPuM3m4fwfxKglr")
model_name = "embed-multilingual-v3.0"
input_type_embed = "search_document"

def get_selected_fields():
    search_key = get_search_key()
    results = get_results()

    df_results = pd.DataFrame(results)
    df_results['combined_text'] = df_results['config'].apply(lambda x: ' '.join(map(str, x))) + ' ' + df_results[
        'name'] + ' ' + df_results['price'].astype(str)

    embeds_combined = co.embed(texts=list(df_results['combined_text']), model=model_name,
                               input_type=input_type_embed).embeddings

    search_index_combined = AnnoyIndex(np.array(embeds_combined).shape[1], 'angular')
    for i in range(len(embeds_combined)):
        search_index_combined.add_item(i, embeds_combined[i])
    search_index_combined.build(10)
    search_index_combined.save('test_combined.ann')

    def get_nearest_neighbors_for_combined(query):
        input_type_query = "search_query"
        query_embed = co.embed(texts=[query], model=model_name, input_type=input_type_query).embeddings
        similar_item_ids = search_index_combined.get_nns_by_vector(query_embed[0], 5, include_distances=False)
        query_results = df_results.iloc[similar_item_ids].copy()
        return query_results

    pd.set_option('display.max_columns', None)

    query = search_key
    combined_nearest_neighbors_result = get_nearest_neighbors_for_combined(query)

    selected_fields = combined_nearest_neighbors_result[['name', 'price', 'link', 'config', 'promo']]

    print(selected_fields.to_string(index=False))

    return selected_fields