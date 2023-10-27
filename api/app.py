from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)

host = "0.0.0.0" if not os.getenv('HBNB_API_HOST') else os.getenv('HBNB_API_HOST')
port = 5000 if not os.getenv('HBNB_API_PORT') else int(os.getenv('HBNB_API_PORT'))

@app.teardown_appcontext
def close_storage(exception):
    """function to carry our clearning and 
    clearing of resources used by web application 
    in the server during the http request"""
    storage.close()

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
