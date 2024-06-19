#!/usr/bin/python3
"""
    Module to create view for the link between Place and Amenity objects
"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from markupsafe import escape
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from os import getenv


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def amenities_by_place(place_id):
    """route to return all Amenity objects of a Place by id"""
    place = storage.get(Place, escape(place_id))
    if not place:
        abort(404)

    amenities_list = [obj.to_dict() for obj in place.amenities]
    return jsonify(amenities_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_of_a_place(place_id, amenity_id):
    """route to delete an Amenity object of a given Place"""
    HBNB_TYPE_STORAGE = getenv('HBNB_TYPE_STORAGE')
    place = storage.get(Place, escape(place_id))
    if not place:
        abort(404)

    amenity = storage.get(Amenity, escape(amenity_id))
    if not amenity:
        abort(404)

    if HBNB_TYPE_STORAGE == 'db' and amenity not in place.amenities:
        abort(404)
    if HBNB_TYPE_STORAGE != 'db' and amenity.id not in place.amenity_ids:
        abort(404)

    if HBNB_TYPE_STORAGE == 'db':
        place.amenities.remove(amenity)
    if HBNB_TYPE_STORAGE != 'db':
        place.amenity_ids.remove(amenity.id)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def add_amenity_to_a_place(place_id, amenity_id):
    """route to add an Amenity to a Place"""
    HBNB_TYPE_STORAGE = getenv('HBNB_TYPE_STORAGE')
    place = storage.get(Place, escape(place_id))
    if not place:
        abort(404)

    amenity = storage.get(Amenity, escape(amenity_id))
    if not amenity:
        abort(404)

    if HBNB_TYPE_STORAGE == 'db' and amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    if HBNB_TYPE_STORAGE != 'db' and amenity.id in place.amenity_ids:
        return jsonify(amenity.to_dict()), 200

    if HBNB_TYPE_STORAGE == 'db':
        place.amenities.append(amenity)
    if HBNB_TYPE_STORAGE != 'db':
        place.amenity_ids.append(amenity.id)

    storage.save()
    return jsonify(amenity.to_dict()), 201
