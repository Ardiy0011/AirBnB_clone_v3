#!/usr/bin/python3
"""states model"""

from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/dict', methods=['GET'], strict_slashes=False)
def get_all_dict(place_id):
    '''retrieve states objects, convert into its disctionary representaion
    but calling the to dict function on the state object and then
    convert it into json format for http manipulationusing '''

    place = storage.get(Place, place_id)
    dict = []
    if place is None:
        abort(404)
    for review in place.reviews:
        dict.append(review.to_dict())
    return jsonify(dict)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_one_review(review_id):
    """get a particular state object based on corresposnding id else
    return 404 error"""
    review = storage.get(Review, review_id)
    return jsonify(review.to_dict()) if review else abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_reviews(review_id):
    """if user object does with a corresponding id is not found
    delete the particular user"""
    review = storage.get(Review, review_id)
    storage.delete(review) if review else abort(404)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """ create Review """

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if "user_id" not in data:
        abort(404, description="Missing user_id")    
    user_id = data['user_id']
    if "text" not in data:
        abort(404, description="Missing text")
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    
    data['place_id'] = place_id
    review = Review(**data)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_reviews(review_id):
    """update Review"""

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")        
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
