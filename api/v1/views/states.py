#!/usr/bin/python3
"""
    Module to create view for State objects
"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from markupsafe import escape


@app_views.route('/states', strict_slashes=False)
def states():
    """route to return all State objects"""
    states_list = [obj.to_dict() for obj in list(storage.all(State).values())]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', strict_slashes=False)
def state_by_id(state_id):
    """route to return all State objects"""
    state = storage.get(State, escape(state_id))
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """route to delete a State object by id"""
    state = storage.get(State, escape(state_id))
    if state:
        state.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state_object():
    """route to add a State object"""
    from models.state import State
    if request.is_json:
        data = request.get_json()
    else:
        abort(400, 'Not a JSON')

    if 'name' not in data:
        abort(400, 'Missing name')

    new_state = State(**data)
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state_object(state_id):
    """route to update a State object by id"""
    state = storage.get(State, escape(state_id))
    if not state:
        abort(404)

    if request.is_json:
        data = request.get_json()
    else:
        abort(400, 'Not a JSON')

    for key in data:
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, data[key])
    state.save()

    return jsonify(state.to_dict()), 200
