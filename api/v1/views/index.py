#!/usr/bin/python3
"""Index file"""
import json
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.user import User
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.amenity import Amenity


@app_views.route('/status', methods=['GET'])
def status():
    """status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """Retrieve the number of each object by type."""
    class_mapping = {
        User: "users",
        City: "cities",
        Place: "places",
        Review: "reviews",
        State: "states",
        Amenity: "amenities"
    }
    stats = {}
    for cls, name in class_mapping.items():
        count = storage.count(cls)
        stats[name] = count
    return json.dumps(stats, indent=4) + '\n'
