#!/usr/bin/python3
"""
View users that handles all default REST API actions
"""
from models import storage
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models.user import User


@app_views.route("/users/", methods=["GET"], strict_slashes=False)
def show_users():
    """Shows a list of all users objects"""
    users = list(storage.all("User").values())
    usr_list = []
    for user in users:
        usr_list.append(user.to_dict())
    return jsonify(usr_list)


@app_views.route("/users/<string:user_id>", methods=["GET"],
                 strict_slashes=False)
def show_user(user_id):
    """Retrieves an User object"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<string:user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a specific user based on id"""
    user = storage.get("User", user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/users/", methods=["POST"], strict_slashes=False)
def post_user():
    """Post an User object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({'error': 'Missing password'}), 400)
    user = User(**request.get_json())
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates an user object by id"""
    user = storage.get("User", user_id)
    err_msg = ""
    if user:
        content = request.get_json(silent=True)
        if type(content) is dict:
            ignore = ["id", "created_at", "updated_at"]
            for name, value in content.items():
                if name not in ignore:
                    setattr(user, name, value)
            storage.save()
            return jsonify(user.to_dict())
        else:
            err_msg = "Not a JSON"
            response = jsonify({"error": err_msg})
            response.status_code = 400
            return response
    abort(404)
