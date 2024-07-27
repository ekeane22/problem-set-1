import json
import requests
from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd
import networkx as nx
from urllib.request import urlopen
from sklearn.metrics import DistanceMetric

def load_information(file_path):
    with open(file_path, 'r') as f:
        data = [json.loads(line) for line in f]
        return data

def df_actor_genre(data):
    actor_genre = {}

    for movie in data:
        genres = movie.get('genres', [])
        actors = movie.get('actors', [])

        for actor in actors:
            actor_id = actor[0]
            actor_name = actor[1]

            if actor_id not in actor_genre:
                actor_genre[actor_id] = {'actor_name': actor_name}

                for genre in genres:
                    if genre not in actor_genre[actor_id]:
                        actor_genre[actor_id][genre] += 1
               
                df_actor_genre = pd.DataFrame.from_dict(actor_genre, orient='index')
                return df_actor_genre

def similiar_actor(df_actor_genre, query_actor_id):
    query_actor = df_actor_genre.loc[query_actor_id].drop('actor.name')
    different_actor = df_actor_genre.drop(query_actor_id)
    
    distance_metric = DistanceMetric.get_metric('cosine')
    e_distance = distance_metric.pairwise[query_actor], different_actor.drop(columns=['actor_name'])
    
    query_actor_id = 'nm0000129'
    query_name = 'Tom Cruise'
    
    similiar_to_query = different_actor.nlargest(10, 'similarity')
    
    return similiar_to_query[['actor_name', 'similiarity']]

def move_to_csv(sim_actor, query_name):
    output_file = Path('output.txt')
    output_file.parent.mdir(parents=True, Exist_ok=True)

    sim_actor.to_csv(output_file, index=False)

    print(f'The similiar actors to ({sim_actor} have been saved to {output_file}')