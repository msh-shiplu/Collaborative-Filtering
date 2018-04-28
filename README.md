# Collaborative Filtering
## Authors:
-   Md Shiplu Hawlader (mhwlader)
-   Alina Zaman (azaman)

## How to run
Python 3 is needed with Numpy and Pandas library installed in the system.
```bash
python3 coll-filter.py
```

Depending on the system the training phase should take 1 - 3 minutes for large input files.
After the training phase the command line will prompt for input with the following suggestions:
```bash
Press 1 to get predicted score
Press 2 to get movie recommendation
Press 3 to test from file
Press anything else to quit
```

If you want to change the training dataset, please pass the new dataset file name with path in the following object creation line:
```python
C = CollaborativeFiltering(train_file="data/ratings.txt", movie_file="data/movie_titles.txt")
```