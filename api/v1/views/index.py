#!/usr/bin/python3
"""file index.py"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status', methods=['GET'])
def status_get():
    """gets the status of the app"""
    return jsonify({"status": "0K"})

@app_views.route('/stats', methods=['GET'])
def get_stats():
    """returns the number of each object by type"""
    obj_list = ['Amenity', 'City', 'Place', 'Review', 'State', 'Users']
    obj_dict = {}
    for obj in obj_list:
        obj_dict[obj] = storage.count(obj)
    return jsonify(obj_dict)
