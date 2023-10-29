from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    status = {'status': 'OK'}
    return jsonify(status)

@app_views.route('/stats', methods=['GET'])
def objectcount():
    """count objects in the class"""
    classes = {"amenity": Amenity, "city": City,
               "place": Place, "review": Review, "state": State, "user": User}
    counter = {}
    for key, value in classes.items():
        counter[key] = storage.count(value)
    return jsonify(counter)
