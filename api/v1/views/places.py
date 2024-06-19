#!/usr/bin/python3
"""
    Module to create view for Place objects
"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from markupsafe import escape


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def places_by_city(city_id):
    """route to return all Place objects of a City by id"""
    city = storage.get(City, escape(city_id))
    if not city:
        abort(404)

    places_list = [obj.to_dict() for obj in city.places]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', strict_slashes=False)
def place_by_id(place_id):
    """route to return a Place object by id"""
    place = storage.get(Place, escape(place_id))
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """route to delete a Place object by id"""
    place = storage.get(Place, escape(place_id))
    if place:
        place.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def add_place_object(city_id):
    """route to add a Place object"""
    city = storage.get(City, escape(city_id))
    if not city:
        abort(404)

    if request.is_json:
        data = request.get_json()
    else:
        abort(400, 'Not a JSON')

    if 'user_id' not in data:
        abort(400, 'Missing user_id')

    user = storage.get(User, escape(data['user_id']))
    if not user:
        abort(404)

    if 'name' not in data:
        abort(400, 'Missing name')

    data['city_id'] = escape(city_id)

    new_place = Place(**data)
    new_place.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place_object(place_id):
    """route to update a Place object by id"""
    place = storage.get(Place, escape(place_id))
    if not place:
        abort(404)

    if request.is_json:
        data = request.get_json()
    else:
        abort(400, 'Not a JSON')

    for key in data:
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, data[key])
    place.save()

    return jsonify(place.to_dict()), 200
