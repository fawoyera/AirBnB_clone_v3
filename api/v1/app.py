#!/usr/bin/python3
"""Module to create flask app"""


from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
import os


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(arg):
    """tear down method"""
    storage.close()


@app.errorhandler(404)
def error_not_found(error):
    """custom 404 error message"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', 5000),
            threaded=True, debug=True)
