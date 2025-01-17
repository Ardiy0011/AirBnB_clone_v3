#!/usr/bin/python3
"""app model"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    """function to carry our clearning and
    clearing of resources used by web application
    in the server during the http request"""
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """json representation of 404 not found code"""
    err = {
        "error": "Not found"
    }
    return jsonify(err), 404


if __name__ == "__main__":
    host = "0.0.0.0" if not getenv(
        'HBNB_API_HOST') else getenv('HBNB_API_HOST')
    port = 5000 if not getenv('HBNB_API_PORT') else int(
        getenv('HBNB_API_PORT'))
    app.run(port=port, host=host, threaded=True)
