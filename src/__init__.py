
from flask import Flask,redirect
from flask.json import jsonify
import os 
from src.auth import auth
from src.bookmarks import bookmarks
from src.database import db,Bookmark
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from flasgger import Swagger, swag_from
from src.config.swagger import template, swagger_config


def create_app():
    app=Flask(__name__,instance_relative_config=True)
    app.config['FLASK_APP']="src"
    app.config['FLASK_ENV']=development
    app.config['SQLALCHEMY_DATABASE_URI']=  'sqlite:///bookmarks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app.config['JWT_SECRET_KEY']='JWT_SECRET_KEY'
    app.config['SECRET_KEY']='SECRET_KEY'
    app.config['SWAGGER']={
        'title': "Bookmarkss API",
        'uiversion':3
    }

    db.app=app
    db.init_app(app)

    JWTManager(app)
    
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)
    Swagger(app,config=swagger_config,template=template)

            
    def redirect_to_url(short_url):
        bookmark=Bookmark.query.filter_by(short_url=short_url).first_or_404()
        if bookmark:
            bookmark.visits=bookmark.visits+1
            db.session.commit()

            return redirect(bookmark.url)

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({
            'error': 'Not found'
        }),HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({
            'error': 'Something went wrong, we are working on it'
        }),HTTP_500_INTERNAL_SERVER_ERROR

    return app
