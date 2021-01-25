import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

with open('dump.html') as f:
    data = f.read()
soup = BeautifulSoup(data, 'html.parser')
link = 'http://www.omdbapi.com/?i={}&apikey={}'

#lists where our data will be stored
imdb_id = []
rank = []
imdb_rating = []
omdb_data = []
csv_columns = []

#function that will find all 'div' tags with 'data-titleid' attribute that contains IMDB ID of a movie
def get_title():
    for div in soup.find_all('div'):
        if div.get('data-titleid') == None:
            continue
        else:
            imdb_id.append(div.get('data-titleid'))
    if len(imdb_id) == 100:
      print ('SUCCESS. Titles received.')

#function that will find all 'span' tags with 'name' attribute. 'rk' means IMDB rank and 'ir' means IMDB rating
def get_rank_rating():
    for span in soup.find_all('span'):
        if span.get('name') == None:
            continue
        elif span.get('name') == 'rk':
            rank.append(span.get('data-value'))
        elif span.get('name') == 'ir':
            imdb_rating.append(span.get('data-value'))
    if len(rank) == 100:
      print ('SUCCESS. Ranks received.')
    if len(imdb_rating) == 100:
      print ('SUCCESS. Ratings received.')

#function that will get data for our movie titles from OMDB in JSON format
def get_omdb_data(api_key):
    for id in imdb_id:
        omdb_json = requests.get(link.format(id, api_key))
        omdb_data.append(omdb_json.json())
    if len(omdb_data) == 100:
      print ('SUCCESS. OMDB data received.')

#function that creates dataframe that we will export in CSV
#please see postscript about it on line 108
def export_to_csv(imdb_id, omdb_data, imdb_rating, rank):
    data = {
        'Rank': rank,
        'ID': imdb_id,
        'Rating': imdb_rating,
        'Title': [x['Title'] for x in omdb_data],
        'Year': [x['Year'] for x in omdb_data],
        'Rated': [x['Rated'] for x in omdb_data],
        'Released': [x['Released'] for x in omdb_data],
        'Runtime': [x['Runtime'] for x in omdb_data],
        'Genre': [x['Genre'] for x in omdb_data],
        'Director': [x['Director'] for x in omdb_data],
        'Writer': [x['Writer'] for x in omdb_data],
        'Actors': [x['Actors'] for x in omdb_data],
        'Plot': [x['Plot'] for x in omdb_data],
        'Language': [x['Language'] for x in omdb_data],
        'Country': [x['Country'] for x in omdb_data],
        'Awards': [x['Awards'] for x in omdb_data],
        'Poster': [x['Poster'] for x in omdb_data],
        'Ratings': [x['Ratings'] for x in omdb_data],
        'Metascore': [x['Metascore'] for x in omdb_data],
        'Ratings': [x['Ratings'] for x in omdb_data],
        'imdbVotes': [x['imdbVotes'] for x in omdb_data],
        'Type': [x['Type'] for x in omdb_data],
        'DVD': [x['DVD'] for x in omdb_data],
        'BoxOffice': [x['BoxOffice'] for x in omdb_data],
        'Production': [x['Production'] for x in omdb_data],
        'Website': [x['Website'] for x in omdb_data],
        'Response': [x['Response'] for x in omdb_data]
    }
    df = pd.DataFrame(data)
    df.to_csv('output.csv')
    print ('SUCCESS. File created.')


#operational part of our code that handles it using terminal
while True:
    api_key = input('Please enter your OMDB Api Key: ')
    if api_key in ['end', 'break', 'quit']:
        print ('Goodbye!')
        break
    else:
         status = requests.get(link.format('tt11161474', api_key))
         status = str(status)
         if status[1:15] != 'Response [200]':
             print ('Sorry. It\'s incorrect.')
             continue
         else:
             print ('SUCCESS. Waiting time: ~30 seconds.')
             get_title()
             get_rank_rating()
             get_omdb_data(api_key)
             export_to_csv(imdb_id, omdb_data, imdb_rating, rank)
             break
f.close()

#originally I wanted to get columns name using get_columns_name() from omdb_data and append it to csv_columns:

#csv_columns = ['Rank', 'IMDB ID', 'Rating']
#def get_columns_name(omdb_data):
#    for column in omdb_data[0]:
#        if column in ['imdbID', 'imdbRating']:
#            continue
#        else:
#             csv_columns.append(column)

#after that the code for export_to_csv() should've looked like this
#def export_to_csv(csv_columns, imdb_id, omdb_data, imdb_rating, rank):
#    lst = []
#    for i in csv_columns:
#      if i == 'Rank':
#        lst.append(rank)
#      elif i == 'IMDB ID':
#        lst.append(imdb_id)
#      elif i == 'Rating':
#        lst.append(imdb_rating)
#      else:
#        v = [x[i] for x in omdb_data]
#        lst.append(v)
#    df = pd.DataFrame(lst, columns=csv_columns)
#    df.to_csv('100.csv')
#    print ('SUCCESS. File created.')

#unfortunately I'm not too familiar with Pandas, hence I had to take that shortcut. Sorry that it isn't as sophisticated
#as I would've hoped it would be. thank you for taking your time to check it out!
