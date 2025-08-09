#!/usr/bin/python3
"""file index.py"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status_get():
    """gets the status of the app"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """returns the number of each object by type"""
    obj_list = {'amenities': 'Amenity', 'cities': 'City',
                'places': 'Place', 'review': 'Review',
                'state': 'State', 'users': 'User'}
    obj_dict = {}
    for obj, obj_name in obj_list.items():
        obj_dict[obj] = storage.count(obj_name)
    return jsonify(obj_dict)
