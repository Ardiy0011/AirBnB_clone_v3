#!/usr/bin/python3
"""cities model"""

from flask import Flask, jsonify, abort, request
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities(state_id):
    """get particular cities in correspondnece to state id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    dict_representation = []
    city_objects = storage.all('City')
    for city in city_objects.values():
        if city.state_id == state_id:
            dict_representation.append(city.to_dict())
    return jsonify(dict_representation)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 trict_slashes=False)
def get_one_city(city_id):
    """retrieve a particular city object based on corresposnding city id else
    return 404 error"""
    particular_city = storage.get(City, city_id)
    if not particular_city:
        abort(404)
    return jsonify(particular_city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """if city  object does with a corresponding cityid is not found
    delete the the  particular state"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """create a new city in with reference to its state_id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, {'error': 'Not a JSON'})
    if "name" not in data:
        abort(400, {'error': 'Missing name'})
    """associate/link state id to the city object
    you created that is found in the json pasrse data"""
    new_city = City(**data)
    new_city.state_id = state_id
    storage.new(new_city)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """update the city object"""
    data = request.get_json()
    if not data:
        abort(400, {'error': 'Not a JSON'})
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
