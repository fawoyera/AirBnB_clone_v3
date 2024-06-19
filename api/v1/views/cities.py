#!/usr/bin/python3
"""
    Module to create view for City objects
"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State
from markupsafe import escape


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def cities_by_state(state_id):
    """route to return all City objects of a State by id"""
    state = storage.get(State, escape(state_id))
    if not state:
        abort(404)

    cities_list = [obj.to_dict() for obj in state.cities]
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def city_by_id(city_id):
    """route to return a City objects by id"""
    city = storage.get(City, escape(city_id))
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city_by_id(city_id):
    """route to delete a City object by id"""
    city = storage.get(City, escape(city_id))
    if city:
        city.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def add_city_object(state_id):
    """route to add a City object"""
    state = storage.get(State, escape(state_id))
    if not state:
        abort(404)

    if request.is_json:
        data = request.get_json()
    else:
        abort(400, 'Not a JSON')

    if 'name' not in data:
        abort(400, 'Missing name')

    data['state_id'] = escape(state_id)

    new_city = City(**data)
    new_city.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city_object(city_id):
    """route to update a City object by id"""
    city = storage.get(City, escape(city_id))
    if not city:
        abort(404)

    if request.is_json:
        data = request.get_json()
    else:
        abort(400, 'Not a JSON')

    for key in data:
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, data[key])
    city.save()

    return jsonify(city.to_dict()), 200
