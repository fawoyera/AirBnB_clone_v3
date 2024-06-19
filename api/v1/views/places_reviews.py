#!/usr/bin/python3
"""
    Module to create view for Review objects
"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from markupsafe import escape
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def reviews_by_place(place_id):
    """route to return all Review objects of a Place by id"""
    place = storage.get(Place, escape(place_id))
    if not place:
        abort(404)

    reviews_list = [obj.to_dict() for obj in place.reviews]
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def review_by_id(review_id):
    """route to return a Review object by id"""
    review = storage.get(Review, escape(review_id))
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review_by_id(review_id):
    """route to delete a Review object by id"""
    review = storage.get(Review, escape(review_id))
    if review:
        review.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def add_review_object(place_id):
    """route to add a Review object"""
    place = storage.get(Place, escape(place_id))
    if not place:
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

    if 'text' not in data:
        abort(400, 'Missing text')

    data['place_id'] = escape(place_id)

    new_review = Review(**data)
    new_review.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review_object(review_id):
    """route to update a Review object by id"""
    review = storage.get(Review, escape(review_id))
    if not review:
        abort(404)

    if request.is_json:
        data = request.get_json()
    else:
        abort(400, 'Not a JSON')

    for key in data:
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review, key, data[key])
    review.save()

    return jsonify(review.to_dict()), 200
