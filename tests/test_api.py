from myapi.models import movie
import requests
import requests_mock as mock
from myapi.library import external_movie_api

#tests without using mock data
def test_search_movie():
	title = ("avengers")
	x = external_movie_api.search_movie(title)
	#assert x != ({'status' : 'down'})
	if x == ({'status':'down'}):
		#send a mail to someone maybe, just for fun
		pass


def test_search_movie_single_mock():
	with mock.Mocker() as m:
		title = ("avengers")
		m.get(m.get('http://www.omdbapi.com/?i=tt3896198&apikey=27f3a92e&t={}'.format(title), json={'Title': "avengers", 'Genre':"genre", 'Plot':"plot" }))
		x = external_movie_api.search_movie(title)
		assert x != ({'status' : 'down'})





def test_search__movie_mock():
	with mock.Mocker() as m:	
		title = ("avengers")
		m.get('http://www.omdbapi.com/?i=tt3896198&apikey=27f3a92e&t={}'.format(title), json={'Title': "avengers", 'Genre':"genre", 'Plot':"plot" })
		#x = external_movie_api.search_movie(title)
		x = requests.get('http://www.omdbapi.com/?i=tt3896198&apikey=27f3a92e&t={}'.format(title))
		print(x)
		assert x != {'status': 'down'}

#actually test the api endpoints
def test_see_all_movies(db, client):
	x = client.get("/see_all_movies")
	assert ("200") in x.status

def test_add_movie(db, client):
	data = {"title": "avengers"}
	x = client.post("/add_movie", json=data)
	
	assert not ("error") in x.json
	


#the cookiecutter actually makes it super duper simple
#to write unit tests damn boi
def test_search_for_movie(db, client):
	with mock.Mocker() as m:
		title = ("avengers")
		db.session.add(movie(Title=title))
		try:
			db.session.commit()
		except:
			db.session.rollback()

		m.get('http://www.omdbapi.com/?i=tt3896198&apikey=27f3a92e&t={}'.format(title), json={
			'Title': "avengers",
			'Genre': "action",
			'Plot': "epic things"
			})
		x = client.get("/search_for_movie?keyword={}".format(title))
		
		assert not ("error") in x.json
		assert ("200") in x.status