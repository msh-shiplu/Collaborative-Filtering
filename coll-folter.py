import numpy as np
import pandas as pd
from datetime import datetime

def calc_similarity(ratings):
    s = ratings.dot(ratings.T) + 1e-9
    norms = np.array([np.sqrt(np.diagonal(s))])
    s = s / norms
    s = s / norms.T
    return s

def calc_predicted_score(ratings, weight):
    avg = ratings.mean(axis=1)
    nratings = (ratings - avg[:, np.newaxis]).copy()
    score = np.divide( weight.dot(nratings), np.array(np.abs(weight).sum(axis=1)).reshape((weight.shape[0], 1)) )
    score += avg[:, np.newaxis]
    return score


if __name__ == "__main__":
    headers = ["movie_id", "user_id", "rating"]
    df = pd.read_csv("ratings.txt", sep=",", names=headers)
    n_users = df.user_id.unique().shape[0]
    n_movies = df.movie_id.unique().shape[0]

    ratings = np.zeros((n_users, n_movies))
    movie_idx, user_idx = 0, 0
    movie_map = {}
    user_map = {}
    for d in df.itertuples():
        if d[1] not in movie_map:
            movie_map[d[1]] = movie_idx
            movie_idx += 1
        if d[2] not in user_map:
            user_map[d[2]] = user_idx
            user_idx += 1

        ratings[user_map[d[2]], movie_map[d[1]]] = d[3]

    headers = ["movie_id", "year_release", "movie_name"]
    df2 = pd.read_csv("movie_titles.txt", sep=",", names=headers, encoding="ISO-8859-1")
    weight = calc_similarity(ratings)
    score = calc_predicted_score(ratings, weight)

    headers = ["movie_id", "year_release", "movie_name"]
    df2 = pd.read_csv("movie_titles.txt", sep=",", names=headers, encoding="ISO-8859-1")
    year_movies = {}
    movie_names = {}
    for d in df2.itertuples():
        if d[1] not in movie_map:
            continue
        if d[2] not in year_movies:
            year_movies[d[2]] = []
        year_movies[d[2]].append(d[1])
        movie_names[d[1]] = d[3]
    while True:
        print("\nPress 1 to get predicted score\nPress 2 to get movie recommendation\nPress anything else to quit\n")
        choice = input("Enter your choice: ")
        if choice == "1":
            user_id = int(input("Enter User ID: "))
            movie_id = int(input("Enter Movie ID: "))
            if user_id not in user_map:
                print("User does not exist!")
            elif movie_id not in movie_map:
                print("No such movie in the database!")
            else:
                print("Predicted score:", score[user_map[user_id]][movie_map[movie_id]])
        elif choice == "2":
            user_id = int(input("Enter User ID: "))
            if user_id not in user_map:
                print("User does not exist!")
                continue
            y = int(input("Enter Release Year: "))
            if y<1900 or y > datetime.now().year:
                print("Invalid Year!!")
                continue
            uid = user_map[user_id]
            mx = -10000
            mxid = -1
            for id in range(movie_idx):
                if ratings[uid][id] == 0:
                    continue
                if score[uid][id] > mx:
                    mx = score[uid][id]
                    mxid = id
            name = None
            for key, value in movie_map.items():
                if value == mxid:
                    name = movie_names[key]
                    movie_id = key
                    break
            if name:
                print("Recommended Movie: ", name + "(" + str(y) + ") [id: " + str(movie_id) + "]")
            else:
                print("No movies to recommend!")
        else:
            print("Good bye!!!")
            break