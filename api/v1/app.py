#!/usr/bin/python3
"""Register blueprint"""
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from os import getenv
from flask_cors import CORS


app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(error):
    """Remove the current SQLAlchemy Session"""
    storage.close()


@app.errorhandler(404)
def not_found(message):
    """Handles the 404 status code"""
    response = jsonify({'error': 'Not found'})
    response.status_code = 404
    return response


if __name__ == '__main__':
    app.run(
        host=getenv('HBNB_API_HOST', default='0.0.0.0'),
        port=int(getenv('HBNB_API_PORT', default=5000)),
        threaded=True
    )
