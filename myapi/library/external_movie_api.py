#!/usr/bin/python
# -*- coding: utf-8 -*
import requests
from time import sleep

def search_movie(title):
	r = requests.get('http://www.omdbapi.com/?i=tt3896198&apikey=27f3a92e&t={}'.format(title))
	if r.status_code == 200:
		api = r.json()
		
		title = api['Title']
		genre = api['Genre']
		plot  = api['Plot']
	else:
		return {'status': "down"}



	return ({
			'title': title,
			'genre': genre,
			'plot': plot
			})



def search_multiple_movies(title):
	r = requests.get('http://www.omdbapi.com/?i=tt3896198&apikey=27f3a92e&s={}'.format(title))
	if r.status_code == 200:
		api = r.json()
		dic = {}
		counter = 0
		for x in api['Search']:
			counter += 1
			title = (x['Title'])
			movie = search_movie(title)
			sleep(0.2)
			dic.update({counter: movie})
		return dic
	else:
		return {'status': "down"}

			
