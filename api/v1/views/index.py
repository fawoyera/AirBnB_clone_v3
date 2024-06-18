#!/usr/bin/python3
"""
    Module to start flask app
"""

from . import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """method to return status of api"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """method to return the no of each objects by type"""
    from models import storage
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.state import State
    from models.user import User
    stat_dict = {"amenities": storage.count(Amenity),
                 "cities": storage.count(City),
                 "places": storage.count(Place),
                 "states": storage.count(State),
                 "users": storage.count(User)}
    return jsonify(stat_dict)
