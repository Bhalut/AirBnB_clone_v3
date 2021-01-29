#!/usr/bin/python3
"""
Flask REST API module
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, render_template, url_for
from models import storage
from flasgger import Swagger
from flask_cors import CORS
import os


app = Flask(__name__)
swagger = Swagger(app)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.url_map.strict_slashes = False

host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """method to handle @app.teardown_appcontext
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """handles 404 errors"""
    code = exception.__str__().split()[0]
    message = {'error': "Not found"}
    return make_response(jsonify(message), code)


if __name__ == "__main__":
    """MAIN"""
    app.run(host=host, port=port, threaded=True)
