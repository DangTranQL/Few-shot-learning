import openai
import umap
import json
import matplotlib.pyplot as plt
import numpy as np
from sentence_transformers import util
import os

# openai.api_key = os.getenv('OpenAI_API_Key')
openai.api_key = "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"
openai.Model.list()

embeddings_location = 'C:/Users/ADMIN/Desktop/mathQ/code/embed_data.json'
questions = 22

def make_embeddings(embeddings_location, questions):
    """
    Takes json files of questions using our json file formatting, 
        embeds them using OpenAI's embedding_engine,
        and saves a new json, embeddings.json, of the embeddings.
    """
    list_of_embeddings = []

    for num in range(1, questions + 1):
        if num < 10:
            q_num = '0' + str(num)
        else:
            q_num = str(num)
        json_location = 'C:/Users/ADMIN/Desktop/mathQ/data/hw2/hw2_Question_' + q_num + '.json'
        with open(json_location, 'r') as f:
            data = json.load(f)
        raw_question = data['Question']
        embedding = openai.Embedding.create(input = raw_question, 
                                            model="text-embedding-ada-002")['data'][0]['embedding']
        list_of_embeddings.append(embedding)

    embeddings = {'list_of_embeddings':list_of_embeddings}
    # print(embeddings)
    with open(embeddings_location, 'w') as f:
        f.write(json.dumps(embeddings))

def get_embeddings(embeddings_file):
    """
    Retrieves embeddings from embeddings_file. Embeddings are assumed to be (n x d).
    """
    with open(embeddings_file, 'r') as f:
        points = json.load(f)['list_of_embeddings']
    return np.array(points)

def get_most_similar(embeddings, i):
    """
    Returns most similar questions, while they are in their embedded form, 
        to the target, index i, via cosine similarity.
    """
    cos_sims = []
    cos_to_num = {}
    for j in range(len(embeddings)):
        cos_sim = util.cos_sim(embeddings[i], embeddings[j]).item()
        cos_to_num[cos_sim] = j
        cos_sims.append(cos_sim)
    ordered = sorted(cos_sims, reverse=True)
    closest_qs = []
    for val in ordered:
        closest_qs.append(cos_to_num[val]+1)
    return closest_qs[1:]

def reduce_via_umap(embeddings, num_dims=2):
    """
    Reduces the dimensionality of the provided embeddings(which are vectors) to num_dims via UMAP.
    If embeddings was an (n x d) numpy array, it will be reduced to a (n x num_dims) numpy array.
    """
    reducer = umap.UMAP(n_components=num_dims)
    reduced = reducer.fit_transform(embeddings)
    return reduced

if __name__ == "__main__":
    make_embeddings(embeddings_location, questions)
    embeddings = get_embeddings(embeddings_location)
    similar = get_most_similar(embeddings, 1)
    print(similar)
    # reduced_points = reduce_via_umap(embeddings)
    # plot_clusters(reduced_points, image_location, questions_per_course=questions_per_course, question_labels=True)
    