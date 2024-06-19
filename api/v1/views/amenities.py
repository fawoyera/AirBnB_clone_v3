#!/usr/bin/python3
"""
    Module to create view for Amenity objects
"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from markupsafe import escape


@app_views.route('/amenities', strict_slashes=False)
def amenities():
    """route to return all Amenity objects"""
    amenities_list = [obj.to_dict() for obj in
                      list(storage.all(Amenity).values())]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def amenity_by_id(amenity_id):
    """route to return an Amenity object by id"""
    amenity = storage.get(Amenity, escape(amenity_id))
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """route to delete an Amenity object by id"""
    amenity = storage.get(Amenity, escape(amenity_id))
    if amenity:
        amenity.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def add_amenity_object():
    """route to add an Amenity object"""
    if request.is_json:
        data = request.get_json()
    else:
        abort(400, 'Not a JSON')

    if 'name' not in data:
        abort(400, 'Missing name')

    new_amenity = Amenity(**data)
    new_amenity.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity_object(amenity_id):
    """route to update an Amenity object by id"""
    amenity = storage.get(Amenity, escape(amenity_id))
    if not amenity:
        abort(404)

    if request.is_json:
        data = request.get_json()
    else:
        abort(400, 'Not a JSON')

    for key in data:
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, data[key])
    amenity.save()

    return jsonify(amenity.to_dict()), 200
