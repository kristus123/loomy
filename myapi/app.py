from flask import Flask

from myapi import auth, api
from myapi.extensions import db, jwt, migrate, celery, mail

from myapi.api.resources.movie import movie_blueprint


def create_app(config=None, testing=False, cli=False):
    """Application factory, used to create application
    """
    app = Flask('myapi')

    configure_app(app, testing)
    configure_extensions(app, cli)
    register_blueprints(app)
    init_celery(app)

    return app


def configure_app(app, testing=False):
    """set configuration for application
    """
    # default configuration
    app.config.from_object('myapi.config')

    if testing is True:
        # override with testing config
        app.config.from_object('myapi.configtest')
    else:
        # override with env variable, fail silently if not set
        app.config.from_envvar("MYAPI_CONFIG", silent=True)


def configure_extensions(app, cli):
    """configure flask extensions
    """
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    if cli is True:
        migrate.init_app(app, db)


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(api.views.blueprint)
    app.register_blueprint(movie_blueprint)


def init_celery(app=None):
    app = app or create_app()
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
