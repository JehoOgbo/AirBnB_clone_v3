#!/usr/bin/python3
"""view for place objects that handles all default api actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def place_list(city_id):
    """retrieves a list of all place objects linked with a city"""
    place_list = storage.all("Place")
    cities_place = []
    for place in place_list.values():
        if place.city_id == city_id:
            cities_place.append(place)
    new_list = []
    for places in cities_place:
        new_list.append(places.to_dict())
    return jsonify(new_list)


@app_views.route('/places/<place_id>', methods=['GET'])
def single_place(place_id):
    """retrieves a single place object"""
    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)
    obj = obj.to_dict()
    return jsonify(obj)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """deletes a place"""
    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """create a new place"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user_id = storage.get("User", user_id)
    if user_id is None:
        abort(404)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_place = Place(**request.get_json())
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/api/v1/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """update a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'city_id',
                        'created_at', 'updated_at']:
            setattr(place, attr, val)
    place.save()
    return jsonify(place.to_dict())
