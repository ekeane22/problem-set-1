'''
PART 1: NETWORK CENTRALITY METRICS

Using the imbd_movies dataset
- Guild a graph and perform some rudimentary graph analysis, extracting centrality metrics from it. 
- Below is some basic code scaffolding that you will need to add to. 
- Tailor this code scaffolding and its stucture to however works to answer the problem
- Make sure the code is line with the standards we're using in this class 
'''
#json == key value pairs
#similiar to a record, but in brackets
#read it in row by row
#The JSON file isn't just one object, but is many JSON objects, which needs a little extra to get it to load in. There're a number of ways to do this.  The jsonlines package is one possible way. Parsing the raw JSON line by 
#line / object by object is another. And likely others as well.
#once i pull it in i can put into a dataframe

import json
import requests
from pathlib import Path
import numpy as np
import pandas as pd
import networkx as nx
from urllib.request import urlopen 
from bs4 import BeautifulSoup

def load_info(file_path):
    with open(file_path, 'r') as f: 
        data = [json.loads(line) for line in f]
        return data
        
def graph(data):
    G = nx.Graph()
    for movie in data: 
            actors = movie.get('actors', [])
            for i, (left_actor_id, left_actor_name) in enumerate(actors):
                G.add_node(left_actor_id, name = left_actor_name)
                for right_actor_id, right_actor_name in actors[i + 1:]:
                    if G.has_edge(left_actor_id, right_actor_id):
                        G[left_actor_id][right_actor_id]["weight"] += 1
                    else: 
                        G.add_edge(left_actor_id, right_actor_id, weight = 1)
                        
    return G
            
def centrality(G):
    degree = dict(nx.degree(G))
    pagerank = nx.pagerank(G)
    closeness = nx.closeness(G)
    betweenness = nx.betweenness(G)
    eigenvector = nx.eigenvector(G)
        
    metrics_df = pd.DataFrame({
        'actor_id': list(degree.keys())
        'degree': list(degree.values())
        'pagerank': list(pagerank.values())
        'closeness': list(closeness.values())
        'betweenness': list(betweenness.values())
        'eigenvector': = list(eigenvector.values())
        })
    return metrics_df

    
def save_to_csv(metrics_df):
    output_file = Path('path to csv')
    output_file.parent.mkdir(parents=True, exist_ok=True)
    metrics_df.to_csv(output_file, index=False)
    print(f'Centrality metrics saved to {output_file}')
    