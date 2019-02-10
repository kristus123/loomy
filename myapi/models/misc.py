from datetime import datetime
from myapi.extensions import db

class add_movie_later(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	original_string = db.Column(db.String(90))
	date_added = db.Column(db.DateTime, default=datetime.now())