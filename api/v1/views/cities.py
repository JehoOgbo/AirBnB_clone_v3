#!/usr/bin/python3
"""view for cities objects that handles all default api actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def cities_list(state_id):
    """retrieves a list of all cities objects of a state"""
    if storage.get("State", state_id) is None:
        abort(404)
    cities_list = storage.all("City")
    state_cities = []
    for city in cities_list.values():
        if city.state_id == state_id:
            state_cities.append(city)
    new_list = []
    for cities in state_cities:
        new_list.append(cities.to_dict())
    return jsonify(new_list)


@app_views.route('/cities/<city_id>', methods=['GET'])
def single_cities(city_id):
    """retrieves a single cities object"""
    obj = storage.get("City", city_id)
    if obj is None:
        abort(404)
    obj = obj.to_dict()
    return jsonify(obj)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_cities(city_id):
    """deletes a cities"""
    obj = storage.get("City", city_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_cities(state_id):
    """creates a new cities object"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in data.keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    data['state_id'] = state_id
    new_cities = City(**data)
    new_cities.save()
    return make_response(jsonify(new_cities.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_cities(city_id):
    """update the information inside a cities object"""
    try:
        data = request.get_json()
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    old = storage.get("City", city_id)
    if old is None:
        abort(404)
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(old, key, value)
    old.save()
    return make_response(jsonify(old.to_dict()), 200)
