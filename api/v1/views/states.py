from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/api/v1/states', methods=['GET'], strict_slashes=False)
def get_states():
    '''retrieve states objects, convert into its disctionary representaion 
    but calling the to dict function on the state object and then
    convert it into json format for http manipulationusing '''
    state_objects = storage.all('State')
    dict_representation = []
    for state in state_objects:
        state_list = state_objects[state]
        dict_representation.append(state_list.to_dict())
    return jsonify(dict_representation)


@app_views.route('/states/<string:state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """get a particular state object based on corresposnding id else
    return 404 error"""
    particular_state = storage.get(State, state_id)
    if not particular_state:
        abort(404)
    dict_representation = particular_state.to_dict()
    return jsonify(dict_representation), 'OK'


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
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

    response = request.get_json()
    if not response:
        abort(400, {'Not a JSON'})
    if "name" not in response:
        abort(400, {'Missing name'})
    return 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state():
    """at this point my brain is too tire to think"""

    return 200
