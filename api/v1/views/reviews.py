#!/usr/bin/python3
"""view for place objects that handles all default api actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def review_list(place_id):
    """retrieves a list of all review objects linked with a place"""
    if storage.get("Place", place_id) is None:
        abort(404)
    review_list = storage.all("Review")
    place_review = []
    for review in review_list.values():
        if review.place_id == place_id:
            place_review.append(review)
    new_list = []
    for reviews in place_review:
        new_list.append(reviews.to_dict())
    return jsonify(new_list)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def single_review(review_id):
    """retrieves a single review object"""
    obj = storage.get("Review", review_id)
    if obj is None:
        abort(404)
    obj = obj.to_dict()
    return jsonify(obj)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_place(review_id):
    """deletes a review"""
    obj = storage.get("Review", review_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """create a new review"""
    place = storage.get("Place", city_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user_id = request.get_json()['user_id']
    if storage.get("User", user_id) is None:
        abort(404)
    if 'text' not in request.get_json():
        return make_response(jsonify({'error': 'Missing text'}), 400)
    data = request.get_json()
    data['place_id'] = place_id
    new_review = Review(**data)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """update a place"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'city_id',
                        'created_at', 'updated_at']:
            setattr(place, attr, val)
    place.save()
    return jsonify(place.to_dict())
