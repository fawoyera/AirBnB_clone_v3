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
