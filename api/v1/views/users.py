#!/usr/bin/python3
"""view for user objects that handles all default api actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def user_list():
    """retrieves a list of all user objects"""
    user_list = storage.all("User")
    new_list = []
    for users in user_list.values():
        new_list.append(users.to_dict())
    return jsonify(new_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def single_user(user_id):
    """retrieves a single user object"""
    obj = storage.get("User", user_id)
    if obj is None:
        abort(404)
    obj = obj.to_dict()
    return jsonify(obj)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """deletes a user"""
    obj = storage.get("User", user_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'])
def create_user():
    """creates a new user"""
    try:
        data = request.get_json()
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in data.keys():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in data.keys():
        return make_response(jsonify({'error': 'Missing password'}), 400)
    new_user = User(**data)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_users(user_id):
    """update the information inside a user object"""
    try:
        data = request.get_json()
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    old = storage.get("User", user_id)
    if old is None:
        abort(404)
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(old, key, value)
    old.save()
    return make_response(jsonify(old.to_dict()), 200)
