#!/usr/bin/python3
"""errorhandling and status page"""


from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    status = {'status': 'OK'}
    return jsonify(status)


@app_views.route('/stats', methods=['GET'])
def objectcount():
    """count objects in the class"""
    from models.engine.db_storage import classes

    counter = {}
    for key in classes:
        value = classes[key]
        counter[key] = storage.count(value)
    return jsonify(counter)
