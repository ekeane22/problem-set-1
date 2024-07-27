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
    '''
    loads the json file line by line.
    
    Args: 
        The path to the json file from the main and data directory.
        
    Returns: 
        dict: list of dictionaries as the json data. 
    '''
    with open(file_path, 'r') as f:
        data = [json.loads(line) for line in f]
        return data

def df_actor_genre(data):
    '''
    Creating a DataFrame. Each row is an actor, each column is a genre, the cells are the calculation of frequency.
    
    Args: 
        data (list of dictionaries): The dict represents the movie, its genre, and the actors. 
        
    Returns: 
        pandas DataFrame: df_actor_genre DataFrame, actors as rows, genres as columns, and frequency. 
    '''
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
    '''
    I tried to find the 10 most similiar actors compared to the query actor. 
    
    Args: 
        df_actor_genre (DataFrame): The pandas dataframe created previously.
        query_actor_id (str): The query actor ID.
    
    Returns: 
        DataFrame: updated dataframe with the 10 similiar actors compared to the query actor. I based this on cosine calculations. 
    '''
    query_actor = df_actor_genre.loc[query_actor_id].drop('actor.name')
    different_actor = df_actor_genre.drop(query_actor_id)
    
    distance_metric = DistanceMetric.get_metric('cosine')
    e_distance = distance_metric.pairwise[query_actor], different_actor.drop(columns=['actor_name'])
    
    query_actor_id = 'nm0000129'
    query_name = 'Tom Cruise'
    
    similiar_to_query = different_actor.nlargest(10, 'similarity')
    
    return similiar_to_query[['actor_name', 'similiarity']]

def move_to_csv(similiar_to_query, query_name):
    '''
    My attempt at saving the dataframe output to a CSV file. It doesnt work. 
    
    Args: 
        similar_to_query: the top 10 actors compared to similiarity.
        query_name (str): The name of the query actor.
    Returns: 
        print statement 
    '''
    output_file = Path('output.txt')
    output_file.parent.mdir(parents=True, Exist_ok=True)

    similiar_to_query.to_csv(output_file, index=False)

    print(f'The similiar actors to ({similiar_to_query} have been saved to {output_file}')