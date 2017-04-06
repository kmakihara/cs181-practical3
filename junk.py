import numpy as np
import pandas as pd
import musicbrainzngs
import numpy as np
import csv
import json

train_file = 'train.csv'
test_file  = 'test.csv'

# Load the training data.
train_data = {}
with open(train_file, 'r') as train_fh:
    train_csv = csv.reader(train_fh, delimiter=',', quotechar='"')
    next(train_csv, None)
    for row in train_csv:
        user   = row[0]
        artist = row[1]
        plays  = int(row[2])
    
        if not user in train_data:
            train_data[user] = {}
        
        train_data[user][artist] = plays

 # load artist genre dictionary
artist_genres_ = pd.read_json('artist_genre.json', typ='series')
artist_genres_dict = dict(artist_genres_)

# get all unique genres
unique_genres = set([genre for genre_list in artist_genres_dict.values() for genre in genre_list]) - set([None])
print len(unique_genres)
print len(np.zeros(len(unique_genres)))
print "train data length", len(train_data)
# create user genre dictionary
user_genres_plays = {}
for row,i in zip(train_data.items(), range(len(train_data))):
	if i == round(len(train_data)/10.0):
		print "10 percent is done..,"
	elif i == round(len(train_data)/3.0):
		print "33 percent is done..."
	elif i == round(len(train_data)/2.0):
		print "50 percent is done..."
	elif i == round(len(train_data)/1.5):
		print "66 percent is done..."
	elif i == round(len(train_data)*0.9):
		print "90 percent is done..."
	user = row[0]
	user_genres_plays[user] = dict(zip(unique_genres, [[] for i in range(len(unique_genres))]))
	for art_plays in row[1].items():
		plays = art_plays[1]
		art = art_plays[0]
		art_gens = artist_genres_dict[art]
		for gen in art_gens:
			if gen != None:
				user_genres_plays[user][gen].append(plays)

with open('user_genre_plays_list.json', 'w') as f:
    json.dump(user_genres_plays, f)
