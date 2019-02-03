from flask_restful import Resource, Api
from myapi.models import movie
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
			#add to a queueue that will run when connection to the api has been confirmed
			# use celery or a db table ? 
			#also send mail to admin so he can confirm that the right movie has bee nadded
			return {'error': 'not possible to add movie right now, but it has been queued up to be added asap'}
		
		check_if_exists = movie.query.filter_by(Title=film['title'])
		if check_if_exists != None:
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
		search = request.args.get('keyword') or ("avengers")
		if search != None:
			film = external_movie_api.search_movie(search)
			if ('status') in film:
				#find a solution
				return {"rip": 'here'}

			elif film != None:
				film = movie.query.filter_by(Title=film['title']).first()
				schema = movie_schema()
				return {"movie": schema.dump(film).data}
			else:
				return {'movie': 'not found'}
				#show recommendations
			
