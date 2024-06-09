#!/usr/bin/python3
""" A module that creates a new view for Amenity objects."""
import json
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects."""
    amenities = storage.all(Amenity).values()
    return make_response(json.dumps(
                         [amenity.to_dict()
                          for amenity in amenities],
                         indent=4) + '\n')


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return make_response(json.dumps(
                         amenity.to_dict(), indent=4) + '\n')


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(json.dumps({}, indent=4) + '\n', 200)


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a Amenity."""
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    amenity = Amenity(**request.json)
    storage.new(amenity)
    storage.save()
    return make_response(json.dumps(
                         amenity.to_dict(), indent=4) + '\n', 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    for key, value in request.json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return make_response(json.dumps(
                         amenity.to_dict(), indent=4) + '\n', 200)
