#   Project: User-User Collaborative Filtering for movies
#   Author : Md Shiplu Hawlader (mhwlader) & Alina Zaman (azaman)

import numpy as np
import pandas as pd
from datetime import datetime


class CollaborativeFiltering:
    def __init__(self, train_file="data/ratings.txt", movie_file="data/movie_titles.txt"):
        self.train_file = train_file
        self.movie_file = movie_file

    def calc_similarity(self, ratings):
        s = ratings.dot(ratings.T) + 1e-9
        norms = np.array([np.sqrt(np.diagonal(s))])
        s = s / norms
        s = s / norms.T
        return s

    def calc_predicted_score(self, ratings, weight):
        avg = ratings.mean(axis=1)
        nratings = (ratings - avg[:, np.newaxis]).copy()
        score = np.divide(weight.dot(nratings), np.array(np.abs(weight).sum(axis=1)).reshape((weight.shape[0], 1)))
        score += avg[:, np.newaxis]
        return score

    def test_from_file(self, file):
        headers = ["movie_id", "user_id", "rating"]
        df = pd.read_csv(file, sep=",", names=headers)
        for d in df.itertuples():
            try:
                print("User ID:", d[2], "Movie ID:", d[1], "Predicted Rating: ",
                      self.score[self.user_map[d[2]]][self.movie_map[d[1]]])
            except Exception:
                print("Error")

    def process(self):
        headers = ["movie_id", "user_id", "rating"]
        df = pd.read_csv(self.train_file, sep=",", names=headers)
        n_users = df.user_id.unique().shape[0]
        n_movies = df.movie_id.unique().shape[0]

        self.ratings = np.zeros((n_users, n_movies))
        self.movie_idx, self.user_idx = 0, 0
        self.movie_map = {}
        self.user_map = {}
        for d in df.itertuples():
            if d[1] not in self.movie_map:
                self.movie_map[d[1]] = self.movie_idx
                self.movie_idx += 1
            if d[2] not in self.user_map:
                self.user_map[d[2]] = self.user_idx
                self.user_idx += 1

            self.ratings[self.user_map[d[2]], self.movie_map[d[1]]] = d[3]

        self.weight = self.calc_similarity(self.ratings)
        self.score = self.calc_predicted_score(self.ratings, self.weight)

        headers = ["movie_id", "year_release", "movie_name"]
        df2 = pd.read_csv(self.movie_file, sep=",", names=headers, encoding="ISO-8859-1")
        year_movies = {}
        movie_names = {}
        for d in df2.itertuples():
            if d[1] not in self.movie_map:
                continue
            if d[2] not in year_movies:
                year_movies[d[2]] = []
            year_movies[d[2]].append(self.movie_map[d[1]])
            movie_names[d[1]] = d[3]
        while True:
            print("\nPress 1 to get predicted score\nPress 2 to get movie recommendation\n"
                  "Press 3 to test from file\nPress anything else to quit\n")
            choice = input("Enter your choice: ")
            if choice == "1":
                user_id = int(input("Enter User ID: "))
                movie_id = int(input("Enter Movie ID: "))
                if user_id not in self.user_map:
                    print("User does not exist!")
                elif movie_id not in self.movie_map:
                    print("No such movie in the database!")
                else:
                    print("Predicted score:", self.score[self.user_map[user_id]][self.movie_map[movie_id]])
            elif choice == "2":
                user_id = int(input("Enter User ID: "))
                if user_id not in self.user_map:
                    print("User does not exist!")
                    continue
                y = int(input("Enter Release Year: "))
                if y < 1900 or y > datetime.now().year:
                    print("Invalid Year!!")
                    continue
                uid = self.user_map[user_id]
                mx = -10000
                mxid = -1
                for id in range(self.movie_idx):
                    if self.ratings[uid][id] == 0 or y not in year_movies or id not in year_movies[y]:
                        continue
                    if self.score[uid][id] > mx:
                        mx = self.score[uid][id]
                        mxid = id
                name = None
                for key, value in self.movie_map.items():
                    if value == mxid:
                        name = movie_names[key]
                        movie_id = key
                        break
                if name:
                    print("Recommended Movie: ", name + "(" + str(y) + ") [id: " + str(movie_id) + "]")
                else:
                    print("No movies to recommend!")
            elif choice == "3":
                filename = input("Enter test file name: ")
                self.test_from_file(filename)
            else:
                print("Good bye!!!")
                break


if __name__ == "__main__":
    C = CollaborativeFiltering(train_file="data/ratings.txt", movie_file="data/movie_titles.txt")
    # C = CollaborativeFiltering(train_file="data_2/train.txt", movie_file="data/movie_titles.txt")
    C.process()