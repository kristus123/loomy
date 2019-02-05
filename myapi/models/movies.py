from datetime import datetime
from myapi.extensions import db


class movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(40))
    desc = db.Column(db.String(255), nullable=False, default=False)
    category = db.Column(db.String(40), nullable=False, default=False)
   

    rental = db.relationship('rental_info', backref='set_rental_info')


class rental_info(db.Model):
    movie = db.Column(db.Integer, db.ForeignKey('movie.id'))
    id = db.Column(db.Integer, primary_key=True)
   
    rented_by = db.Column(db.Integer, db.ForeignKey('user_v2.id'))
   
    rented_to   = db.Column(db.DateTime)