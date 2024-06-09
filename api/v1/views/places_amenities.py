#!/usr/bin/python3
"""Place-Amenity view module."""
import json
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = place.amenities if storage_t == 'db' else [
        storage.get(Amenity, id) for id in place.amenity_ids]
    return make_response(json.dumps(
        [amenity.to_dict() for amenity in amenities], indent=4) + '\n')


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes an Amenity object from a Place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if storage_t == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return make_response(json.dumps({}, indent=4) + '\n', 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """Links an Amenity object to a Place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if storage_t == 'db':
        if amenity in place.amenities:
            return make_response(
                json.dumps(
                    amenity.to_dict(),
                    indent=4) + '\n',
                200)
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(
                json.dumps(
                    amenity.to_dict(),
                    indent=4) + '\n',
                200)
        place.amenity_ids.append(amenity_id)
    storage.save()
    return make_response(json.dumps(amenity.to_dict(), indent=4) + '\n', 201)
