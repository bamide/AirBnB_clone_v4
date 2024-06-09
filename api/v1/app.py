#!/usr/bin/python3
"""Module that defines the app"""
import json
from flask import Flask, jsonify, make_response
from flask_cors import CORS
import os
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(exception=None):
    """close storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Return a custom message for 404 errors."""
    response = make_response(
                             json.dumps(
                                        {"error": "Not found"},
                                        indent=4) + '\n', 404)
    response.mimetype = "application/json"
    return response


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
