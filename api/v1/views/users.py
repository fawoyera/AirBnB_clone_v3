#!/usr/bin/python3
"""
    Module to create view for User objects
"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from markupsafe import escape


@app_views.route('/users', strict_slashes=False)
def users():
    """route to return all User objects"""
    users_list = [obj.to_dict() for obj in
                  list(storage.all(User).values())]
    return jsonify(users_list)


@app_views.route('/users/<user_id>', strict_slashes=False)
def user_by_id(user_id):
    """route to return a User object by id"""
    user = storage.get(User, escape(user_id))
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user_by_id(user_id):
    """route to delete a User object by id"""
    user = storage.get(User, escape(user_id))
    if user:
        user.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user_object():
    """route to add a User object"""
    if request.is_json:
        data = request.get_json()
    else:
        abort(400, 'Not a JSON')

    if 'email' not in data:
        abort(400, 'Missing email')

    if 'password' not in data:
        abort(400, 'Missing password')

    new_user = User(**data)
    new_user.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user_object(user_id):
    """route to update a User object by id"""
    user = storage.get(User, escape(user_id))
    if not user:
        abort(404)

    if request.is_json:
        data = request.get_json()
    else:
        abort(400, 'Not a JSON')

    for key in data:
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, data[key])
    user.save()

    return jsonify(user.to_dict()), 200
