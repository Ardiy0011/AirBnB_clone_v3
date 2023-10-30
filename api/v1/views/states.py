#!/usr/bin/python3
"""states model"""

from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    '''retrieve states objects, convert into its disctionary representaion
    but calling the to dict function on the state object and then
    convert it into json format for http manipulationusing '''

    state_objects = storage.all('State')
    dict_representation = []
    for state in state_objects.values():
        dict_representation.append(state.to_dict())
    return jsonify(dict_representation)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_one_state(state_id):
    """get a particular state object based on corresposnding id else
    return 404 error"""

    particular_state = storage.get(State, state_id)
    if particular_state is None:
        abort(404)
    dict_representation = particular_state.to_dict()
    return jsonify(dict_representation), 200


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """if state object does with a corresponding id is not found
    delete the the  particular state"""
    particular_state = storage.get(State, state_id)
    if not particular_state:
        abort(404)
    storage.delete(particular_state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """at this point my brain is too tire to think"""

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    state = State(name=data['name'])
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """at this point my brain is too tire to think"""

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"message": "Not a JSON"}), 400
    ignored = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignored:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
