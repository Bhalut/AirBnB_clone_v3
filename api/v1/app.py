#!/usr/bin/python3
""" app

    Flask REST API module
"""
from flask import Flask, Blueprint, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def close(error):
    """ Call method close() from storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Response for error code 404

    Args:
        error

    Returns:
        response
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host, port, threaded=True)
