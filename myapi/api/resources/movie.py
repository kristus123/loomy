from datetime import datetime
from flask_restful import Resource, Api
from myapi.models import movie, User, rental_info
from flask import Blueprint, request
from myapi.extensions import ma, db
from myapi.library import external_movie_api, commit




movie_blueprint = Blueprint('movie_blueprint', __name__)
api = Api(movie_blueprint)



class movie_schema(ma.ModelSchema):
	class Meta:
		model = movie




@api.resource("/see_all_movies")
class see_all_movies(Resource):
	def get(self):
		schema = movie_schema(many=True)
		all_movies = movie.query.all()
		commit()
		return {'movies': schema.dump(all_movies).data}




@api.resource('/add_movie')
class add_movie(Resource):
	def post(self):
		r = request.get_json()
		title = r['title'] 
		#movie_info = {'status': "down"}
		movie_info = external_movie_api.search_movie(title)
		if ('status') in movie_info:
			return {'error': 'not possible to add movie right now, but it has been queued up to be added asap'}
		
		check_if_exists = movie.query.filter_by(Title=movie_info['title']).first()
		if check_if_exists == None:
			new_movie = movie(Title=movie_info['title'], desc=movie_info['plot'], category=movie_info['genre'])
			db.session.add(new_movie)
			try:
				db.session.commit()
			except:
				db.session.rollback()
			return {'title': new_movie.id}
		else:
			return {'movie already added': str(check_if_exists.Title)}




@api.resource("/search_for_movie")
class search_for_movie(Resource):
	def get(self):
		search = request.args.get('keyword')
		#return {'2': str(search)}
		if search != None:
			film = external_movie_api.search_movie(search)
			if ('status') in film:
				#find a solution
				return {"rip": 'here'}

			elif film != None:
				film = movie.query.filter_by(Title=film['title']).first()
				if film == None:
					return {'movie': 'not found'}


				schema = movie_schema()
				return {"movie": schema.dump(film).data}
			
				#show recommendations
			

@api.resource("/rent_movie")
class rent_movie(Resource):
	def put(self):
		title = request.args.get('title')

		movie_info = external_movie_api.search_movie(title)
		film = movie.query.filter_by(Title=movie_info['title']).first()
		if not film:
			return ("movie not found")
		if not film.rental:
			bruker = User.query.first() #temporary solution
			rental = rental_info(movie=film.id, rented_by=bruker.id, rented_to=datetime.utcnow())
			db.session.add(rental)
			db.session.commit()
			return str(rental)
		else:
			return "movie already rented "