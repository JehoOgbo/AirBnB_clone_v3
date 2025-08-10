#!/usr/bin/python3
"""view for cities objects that handles all default api actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.cities import cities


@app_views.route('/cities', methods=['GET'])
def cities_list():
    """retrieves a list of all cities objects"""
    cities_list = storage.all("cities")
    new_list = []
    for cities in cities_list.values():
        new_list.append(cities.to_dict())
    return jsonify(new_list)


@app_views.route('/cities/<cities_id>', methods=['GET'])
def single_cities(cities_id):
    """retrieves a single cities object"""
    obj = storage.get("cities", cities_id)
    if obj is None:
        abort(404)
    obj = obj.to_dict()
    return jsonify(obj)


@app_views.route('/cities/<cities_id>', methods=['DELETE'])
def delete_cities(cities_id):
    """deletes a cities"""
    obj = storage.get("cities", cities_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({})


@app_views.route('/cities', methods=['POST'])
def create_cities():
    """creates a new cities object"""
    try:
        data = request.get_json()
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in data.keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_cities = cities(**data)
    new_cities.save()
    return make_response(jsonify(new_cities.to_dict()), 201)


@app_views.route('/cities/<cities_id>', methods=['PUT'])
def update_cities(cities_id):
    """update the information inside a cities object"""
    try:
        data = request.get_json()
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    old = storage.get("cities", cities_id)
    if old is None:
        abort(404)
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(old, key, value)
    old.save()
    new = storage.get("cities", cities_id)
    return make_response(jsonify(new.to_dict()), 200)
