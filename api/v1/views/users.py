#!/usr/bin/python3
"""User view module."""
import json
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects."""
    users = storage.all(User).values()
    return make_response(json.dumps(
                         [user.to_dict() for user in users], indent=4) + '\n')


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return make_response(json.dumps(user.to_dict(), indent=4) + '\n')


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(json.dumps({}, indent=4) + '\n', 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User."""
    if not request.json:
        abort(400, description="Not a JSON")
    if 'email' not in request.json:
        abort(400, description="Missing email")
    if 'password' not in request.json:
        abort(400, description="Missing password")
    user = User(**request.json)
    storage.new(user)
    storage.save()
    return make_response(json.dumps(user.to_dict(), indent=4) + '\n', 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    for key, value in request.json.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return make_response(json.dumps(user.to_dict(), indent=4) + '\n', 200)
