import pandas as pd
import requests
import json, re
from random import randint
import tweepy
from ConfigParser import *

""" Twitter Bot that tweets random books & whisky combinations"""

#load credentials
config = ConfigParser()
config.read('config.ini')

nyt_key = config.get('nyt', 'NYT_KEY')

#pass key as param
def get_books_from_nyt(nyt_key):
    global title
    url = str('https://api.nytimes.com/svc/books/v3/lists.json?api-key=' + nyt_key + '&list=hardcover-fiction&weeks-on-list=1')
    r = requests.get(url)
    response = r.json()
    response_dict = response['results']
    s = pd.DataFrame(response_dict)
    book_number = randint(0,len(s.index))
    book_details = s['book_details'][book_number]
    title = re.search('u\'title\': u\'(.*?)\', ', str(book_details)).group(1)
    return title

#potentially integrate url

def get_whisky():
    global whisky
    whisky_data = pd.read_csv("whisky_api.csv")
    whisky_number = randint(0,len(whisky_data.index))
    whisky = whisky_data['Whisky'][whisky_number]
    return whisky


def create_a_tweet():
    global tweet
    intro_list = ["Tonight you might want to consider" ,  "All the book worms prefer ", "Personally verified and highly recommended ", "Just another combo ", " Bad day? Try "]
    intro_phrase = intro_list[randint(0,len(intro_list))]
    tweet = str(intro_phrase + whisky + " and " + title + " #booksandwhisky")

def get_api():
  auth = tweepy.OAuthHandler(config.get('twitter', 'consumer_key'), config.get('twitter', 'consumer_secret'))
  auth.set_access_token(config.get('twitter', 'access_token'), config.get('twitter', 'access_token_secret'))
  return tweepy.API(auth)

def post_the_tweet():
    api = get_api()
    status = api.update_status(status=tweet) 
    print("success entry")


if __name__ == "__main__":
    get_books_from_nyt(nyt_key)
    get_whisky()
    create_a_tweet()
    if len(tweet) <= 140:
        print("all good")
        post_the_tweet()
    else:
        print("too long")


