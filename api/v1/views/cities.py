#!/usr/bin/python3
""" A module that creates a new view for City objects."""
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State, City


@app_views.route(
        '/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """Retrieve all City objects of a State."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = storage.all(City).values()
    state_cities = [city for city in cities if city.state_id == state_id]
    return jsonify([city.to_dict() for city in state_cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieve a City object by ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route(
        '/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete a City object by Id."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Create a new City object."""
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    new_city = City(name=data['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update a City object."""
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
