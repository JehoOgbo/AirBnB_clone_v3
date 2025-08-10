#!/usr/bin/python3
"""view for state objects that handles all default api actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def states_list():
    """retrieves a list of all state objects"""
    state_list = storage.all("State")
    new_list = []
    for state in state_list.values():
        new_list.append(state.to_dict())
    return jsonify(new_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def single_state(state_id):
    """retrieves a single state object"""
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    obj = obj.to_dict()
    return jsonify(obj)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """deletes a state"""
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'])
def create_state():
    """creates a new state object"""
    try:
        data = request.get_json()
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in data.keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_state = State(**data)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """update the information inside a state object"""
    try:
        data = request.get_json()
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    old = storage.get("State", state_id)
    if old is None:
        abort(404)
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(old, key, value)
    old.save()
    new = storage.get("State", state_id)
    return make_response(jsonify(new.to_dict()), 200)
