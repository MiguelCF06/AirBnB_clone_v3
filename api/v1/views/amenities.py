#!/usr/bin/python3
"""
View amenities that handles all default REST API actions
"""
from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.city import City
from models.state import State


@app_views.route("/amenities/", methods=["GET"], strict_slashes=False)
def show_amenities():
    """Shows a list of all amenity objects"""
    amenities = list(storage.all("Amenity").values())
    amts_list = []
    for amenity in amenities:
        amts_list.append(amenity.to_dict())
    return jsonify(amts_list)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def show_amenity(amenity_id):
    """Retrieves a Amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<string:amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an specific amenity based on id"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Post an amenity object"""
    content = request.get_json(silent=True)
    error_message = ""
    if type(content) is dict:
        if "name" in content.keys():
            amenity = Amenity(**content)
            storage.new(amenity)
            storage.save()
            response = jsonify(amenity.to_dict())
            response.status_code = 201
            return response
        else:
            error_message = "Missing name"
    else:
        error_message = "Not a JSON"
    response = jsonify({"error": error_message})
    response.status_code = 400
    return response


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an amenity object by id"""
    amenity = storage.get("Amenity", amenity_id)
    err_msg = ""
    if amenity:
        content = request.get_json(silent=True)
        if type(content) is dict:
            ignore = ["id", "created_at", "updated_at"]
            for name, value in content.items():
                if name not in ignore:
                    setattr(amenity, name, value)
            storage.save()
            return jsonify(amenity.to_dict())
        else:
            err_msg = "Not a JSON"
            response = jsonify({"error": err_msg})
            response.status_code = 400
            return response
    abort(404)
