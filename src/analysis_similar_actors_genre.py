'''
PART 2: SIMILAR ACTROS BY GENRE
Using the imbd_movies dataset:
- Create a data frame, where each row corresponds to an actor, each column represents a genre, and each cell captures how many times that row's actor has appeared in that column’s genre 
- Using this data frame as your “feature matrix”, select an actor (called your “query”) for whom you want to find the top 10 most similar actors based on the genres in which they’ve starred 
- - As an example, select the row from your data frame associated with Chris Hemsworth, actor ID “nm1165110”, as your “query” actor
- Use sklearn.metrics.DistanceMetric to calculate the euclidean distances between your query actor and all other actors based on their genre appearances
- - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.DistanceMetric.html
- Output a CSV continaing the top ten actors most similar to your query actor using cosine distance 
- - Name it 'similar_actors_genre_{current_datetime}.csv' to `/data`
- - For example, the top 10 for Chris Hemsworth are:  
        nm1165110 Chris Hemsworth
        nm0000129 Tom Cruise
        nm0147147 Henry Cavill
        nm0829032 Ray Stevenson
        nm5899377 Tiger Shroff
        nm1679372 Sudeep
        nm0003244 Jordi Mollà
        nm0636280 Richard Norton
        nm0607884 Mark Mortimer
        nm2018237 Taylor Kitsch
- Describe in a print() statement how this list changes based on Euclidean distance
- Make sure your code is in line with the standards we're using in this class
'''

#Write your code below
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
                        actor_genre[actor_id][genre] = 0
                        actor_genre[actor_id][genre] += 1
                df_actor_genre = pd.DataFrame.from_dict(actor_genre, orient='index').fillna(0)
                return df_actor_genre


def similiar_actor(df_actor_genre, query_actor_id):
    # find top 10 actors to the query actor based on genre
    query_actor = df_actor_genre.loc[query_actor_id].drop('actor.name').values
    other_actor = df_actor_genre.drop(query_actor_id)
    metric = DistanceMetric.get_metric('cosine')
    distance = metric.pairwise([query_actor], other_actor.drop(columns=['actor_name']).values)[0]
    other_actor['similiarity'] = 1 - distance
    sim = other_actor.nlargest(10, 'similarity')
    return sim[['actor_name', 'similarity']]


def move_to_csv(sim_actor, query_name):
    time = datetime.now.strftime('%m/%d %H:%M')
    print(time)
    output_file = Path('output.txt')
    output_file.parent.mdir(parents=True, Exist_ok=True)

    sim_actor.to_csv(output_file, index=False)

    print(f'The similiar actors to ({sim_actor} have been saved to {output_file}')

# do i need this? i dont think so 
def main():
    # data_filepath = Path(path)
    data_filepath = 'imdb_movies.json'
    data = load_information(data_filepath)
    actor_genre = df_actor_genre(data)
    print(actor_genre)
    # query_actor_id =  # enter actor ID from example above


if __name__ == '__main__':
    main()

