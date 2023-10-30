#!/usr/bin/python3
"""states model"""

from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    '''retrieve states objects, convert into its disctionary representaion
    but calling the to dict function on the state object and then
    convert it into json format for http manipulationusing '''

    user_objects = storage.all('User')
    dict_representation = []
    for user in user_objects.values():
        dict_representation.append(user.to_dict())
    return jsonify(dict_representation)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_one_user(user_id):
    """get a particular state object based on corresposnding id else
    return 404 error"""
    user = storage.get(State, user_id)
    return jsonify(user.to_dict()) if user else abort(404)


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """if user object does with a corresponding id is not found
    delete the particular user"""
    user = storage.get(State, user_id)
    storage.delete(user) if user else abort(404)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """at this point my brain is too tire to think"""

    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if "email" not in data:
        abort(404, description="Missing email")
    if "password" not in data:
        abort(404, description="Missing password")
    user = User(**data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """at this point my brain is too tire to think"""

    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    ignore = ['id', 'email', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
