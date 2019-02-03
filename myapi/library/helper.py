from myapi.extensions import db

def commit():
	try:
		db.session.commit()
	except:
		db.session.rollback()