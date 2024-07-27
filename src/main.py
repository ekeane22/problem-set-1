import json
import requests
import numpy as np
import pandas as pd
import networkx as nx
from urllib.request import urlopen
from bs4 import BeautifulSoup
import jsonlines
import analysis_network_centrality as anc
import analysis_similar_actors_genre as sag

url = "https://github.com/cbuntain/umd.inst414/blob/main/data/imdb_movies_2000to2022.prolific.json?raw=true"
filename = '../data/imdb_movies_2000to2022.prolific.json'


def download_json(url):
    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'w+') as temp_file:
        temp_file.write(response.text)

def load_json():
    data = []
    datalines = jsonlines.open(filename, 'r')
    for line in datalines:
        data.append(line)
    return data

def main():
    download_json(url)
    data = load_json()
    print(data)

metrics_df = anc.analysis(anc.data)
anc.to_csv(metrics_df, '../data/network_centrality_metrics.csv')

df_actor_genre = sag.analysis(sag.data)

sag.to_csv(df_actor_genre, '../data/analysis.similiar.actors.genre.csv')

if __name__ == "__main__":
    main()