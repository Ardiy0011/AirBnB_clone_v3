#!/usr/bin/python3
"""place model"""

from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    '''retrieve places objects, convert into its disctionary representaion
    but calling the to dict function on the state object and then
    convert it into json format for http manipulationusing '''

    city = storage.get(City, city_id)
    dict = []
    if city is None:
        abort(404)
    for place in city.places:
        dict.append(place.to_dict())
    return jsonify(dict)


@app_views.route('places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_a_place(place_id):
    """get a particular state object based on corresposnding id else
    return 404 error"""
    place = storage.get(Place, place_id)
    return jsonify(place.to_dict()) if place else abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """if Place object does with a corresponding id is not found
    delete the particular Place"""
    Place = storage.get(Place, place_id)
    storage.delete(Place) if Place else abort(404)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_Place(city_id):
    """at this point my brain is too tire to think"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")

    if "user_id" not in data:
        abort(404, description="Missing user_id")
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if "name" not in data:
        abort(404, description="Missing name")
    data['city_id'] = city_id

    place = Place(**data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_Place(place_id):
    """at this point my brain is too tire to think"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    ignore = ['id', 'email', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
