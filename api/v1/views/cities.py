#!/usr/bin/python3
"""
View Cities that handles all default REST API actions
"""

from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.city import City
from models.state import State


@app_views.route("/states/<string:state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def show_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get("State", state_id)
    if state is not None:
        cities = []
        for city in state.cities:
            cities.append(city.to_dict())
        return jsonify(cities)
    else:
        abort(404)


@app_views.route("/cities/<string:city_id>", methods=["GET"],
                 strict_slashes=False)
def show_city(city_id):
    """Retrieves a City object."""
    city = storage.get("City", city_id)
    if city is not None:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route("/cities/<string:city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get("City", city_id)
    if city is not None:
        city.delete()
        storage.save()
        return (jsonify({}))
    else:
        abort(404)


@app_views.route("/states/<string:state_id>/cities/", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City"""
    state = storage.get("State", state_id)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    if state is None:
        abort(404)
    k_v = request.get_json()
    k_v["state_id"] = state_id
    city = City(**k_v)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def updates_city(city_id):
    """Updates a City object"""
    city = storage.get("City", city_id)
    if city is not None:
        for attr, val in request.get_json().items():
            if attr not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(city, attr, val)
        city.save()
        return jsonify(city.to_dict())
    else:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
