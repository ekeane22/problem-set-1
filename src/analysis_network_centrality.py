import json
import requests
from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd
import jsonlines 
import networkx as nx
from urllib.request import urlopen
from sklearn.metrics import DistanceMetric

def load_info(file_path):
    with open(file_path, 'r') as f: 
        data = [json.loads(line) for line in f]
        return data 
        
def graph(data):
    g = nx.Graph()
    for movie in data: 
            actors = movie.get('actors', [])
            for i, (left_actor_id, left_actor_name) in enumerate(actors):
                g.add_node(left_actor_id, name = left_actor_name)
                
                for right_actor_id, right_actor_name in actors[i + 1:]:
                    g.add_node(right_actor_id, name=right_actor_name)
                    
                    if g.has_edge(left_actor_id, right_actor_id):
                        g[left_actor_id][right_actor_id]["weight"] += 1
                    else: 
                        g.add_edge(left_actor_id, right_actor_id, weight = 1)        
    return g
            
def centrality(g):
    degree = dict(nx.degree(g))
    pagerank = nx.pagerank(g)
    closeness = nx.closeness(g)
    betweenness = nx.betweenness(g)
    eigenvector = nx.eigenvector(g)
        
    metrics_df = pd.DataFrame({
        'actor_id': list(degree.keys()),
        'degree': list(degree.values()),
        'pagerank': list(pagerank.values()),
        'closeness': list(closeness.values()),
        'betweenness': list(betweenness.values()),
        'eigenvector': list(eigenvector.values())
        })
    return metrics_df

def analysis(graph, data):
    g = graph(data)
    metrics_df = centrality(g)

def save_to_csv(metrics_df, output_file):
    output_file = Path('../data/network_centrality_metrics.csv')
    output_file.parent.mkdir(parents=True, exist_ok=True)
    metrics_df.to_csv(output_file, index=False)
    print(f'Centrality metrics saved to {output_file}') 