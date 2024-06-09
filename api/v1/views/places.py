#!/usr/bin/python3
"""Place view module."""
import json
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    return make_response(json.dumps([place.to_dict()
                         for place in places], indent=4) + '\n')


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return make_response(json.dumps(place.to_dict(), indent=4) + '\n')


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(json.dumps({}, indent=4) + '\n', 200)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    if 'user_id' not in request.json:
        abort(400, description="Missing user_id")
    user = storage.get(User, request.json['user_id'])
    if user is None:
        abort(404)
    if 'name' not in request.json:
        abort(400, description="Missing name")
    request.json['city_id'] = city_id
    place = Place(**request.json)
    storage.new(place)
    storage.save()
    return make_response(json.dumps(place.to_dict(), indent=4) + '\n', 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    for key, value in request.json.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return make_response(json.dumps(place.to_dict(), indent=4) + '\n', 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Retrieves all Place objects depending on
    the JSON in the body of the request."""
    if not request.json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    if not data or all(
        not data[key] for key in [
            'states',
            'cities',
            'amenities']):
        places = storage.all(Place).values()
    else:
        places = []
        if 'states' in data and data['states']:
            for state_id in data['states']:
                state = storage.get(State, state_id)
                if state:
                    for city in state.cities:
                        places.extend(city.places)
        if 'cities' in data and data['cities']:
            for city_id in data['cities']:
                city = storage.get(City, city_id)
                if city:
                    places.extend(city.places)
        places = list(set(places))  # Remove duplicates

        if 'amenities' in data and data['amenities']:
            amenities = [storage.get(Amenity, amenity_id)
                         for amenity_id in data['amenities']]
            places = [
                place for place in places if all(
                    amenity in place.amenities for amenity in amenities)]

    return make_response(json.dumps([place.to_dict()
                         for place in places], indent=4) + '\n')
