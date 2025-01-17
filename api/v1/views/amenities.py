#!/usr/bin/python3
"""amenities model"""

from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_all_amenities():
    '''retrieve amenity objects, convert into its disctionary representaion
    but calling the to dict function on the state object and then
    convert it into json format for http manipulationusing '''

    amenity_objects = storage.all('Amenity')
    dict_representation = []
    for amenity in amenity_objects.values():
        dict_representation.append(amenity.to_dict())
    return jsonify(dict_representation)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_one_amenity(amenity_id):
    """get a particular state object based on corresposnding id else
    return 404 error"""

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """if state object does with a corresponding id is not found
    delete the the  particular amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """at this point my brain is too tire to think"""

    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if "name" not in data:
        abort(400, description="Missing name")
    amenity = Amenity(name=data['name'])
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenities(amenity_id):
    """at this point my brain is too tire to think"""

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"message": "Not a JSON"}), 400
    ignored = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignored:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
