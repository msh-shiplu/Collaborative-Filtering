
movies_id_title = {}
movies_id_year = {}
movies_year_id = {}
user_movies = {}
weight = {}
ratings = {}
average_ratings = {}
total = {}


def read_movie_details(file):
    f = open(file)
    l = f.readline()
    while l:
        t = l.split(sep=",")
        title = ",".join(l[2:])
        movies_id_title[t[0]] = title
        movies_id_year[t[0]] = t[1]
        movies_year_id[t[1]] = t[0]
        l = f.readline()


def read_ratings(file):
    f = open(file)
    l = f.readline()
    while l:
        movie_id, user_id, r = l.split(sep=",")
        if user_id not in user_movies:
            user_movies[user_id] = []
        user_movies[user_id].append(movie_id)
        r = float(r)
        if movie_id not in ratings:
            ratings[movie_id] = []
        ratings[movie_id].append((user_id, r))

        if user_id not in average_ratings:
            average_ratings[user_id] = 0
            total[user_id] = 0

        average_ratings[user_id] += r
        total[user_id] += 1
        l = f.readline()

def precalculate():
    for user_id in average_ratings.keys():
        average_ratings[user_id] /= total[user_id]

    for movie_id, L in ratings.items():
        for i in range(len(L)):
            user1 = L[i][0]
            r1 = L[i][1]
            if user1 not in weight:
                weight[user1] = {}

            for j in range(len(L)):
                user2 = L[j][0]
                r2 = L[j][1]
                if user2 not in weight[user1]:
                    weight[user1][user2] = 0
                weight[user1][user2] += (r1 - average_ratings[user1])*(r2 - average_ratings[user2])

    for u in weight.keys():
        for v in weight[u].keys():
            weight[u][v] /= (weight[u][u]*weight[v][v])


def get_predicted_score(user_id, movie_id):
    score = 0
    for l in ratings[movie_id]:
        u = l[0]
        r = l[1]
        score += weight[user_id][u]*(r - average_ratings[u])
        sum += abs(weight[user_id][u])

    score += average_ratings[user_id]
    return score


if __name__ == "__main__":
    read_movie_details("movie_titles.txt")
    read_ratings("ratings.txt")
    precalculate()
    user_id = input("Enter user id: ")
    movie_id = input("Enter movie id")
    if movie_id in user_movies[user_id]:
        print("User already rated the movie")
    else:
        print(get_predicted_score(user_id, movie_id))
