from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    status = {'status': 'OK'}
    return jsonify(status)

@app_views.route('/api/v1/stats', methods=['GET'])
def objectcount():
    from models.engine.db_storage import classes

    counter = {}
    for key in classes:
        value = classes[key]
        counter[key] = storage.count(value)
    return jsonify(counter)
