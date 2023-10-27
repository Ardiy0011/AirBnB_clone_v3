from flask import Flask, jsonify, request
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def close_storage(exception):
    """function to carry our clearning and 
    clearing of resources used by web application 
    in the server during the http request"""
    storage.close()


if __name__ == "__main__":
    host = "0.0.0.0" if not getenv('HBNB_API_HOST') else getenv('HBNB_API_HOST')
    port = 5000 if not getenv('HBNB_API_PORT') else int(getenv('HBNB_API_PORT'))
    app.run(port=port, host=host, threaded=True)
