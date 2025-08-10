#!/usr/bin/python3
"""view for amenities objects that handles all default api actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def amenities_list():
    """retrieves a list of all amenities objects"""
    amenities_list = storage.all("Amenity")
    new_list = []
    for amenities in amenities_list.values():
        new_list.append(amenities.to_dict())
    return jsonify(new_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def single_amenities(amenity_id):
    """retrieves a single amenities object"""
    obj = storage.get("Amenity", amenity_id)
    if obj is None:
        abort(404)
    obj = obj.to_dict()
    return jsonify(obj)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenities(amenity_id):
    """deletes an amenities"""
    obj = storage.get("Amenity", amenity_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'])
def create_amenities():
    """creates a new amenities object"""
    try:
        data = request.get_json()
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in data.keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_amenities = Amenity(**data)
    new_amenities.save()
    return make_response(jsonify(new_amenities.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenities(amenity_id):
    """update the information inside a amenities object"""
    try:
        data = request.get_json()
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    old = storage.get("Amenity", amenity_id)
    if old is None:
        abort(404)
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(old, key, value)
    old.save()
    return make_response(jsonify(old.to_dict()), 200)
