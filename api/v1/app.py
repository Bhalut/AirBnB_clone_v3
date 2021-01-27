#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, render_template, url_for
from models import storage
from flasgger import Swagger
import os


app = Flask(__name__)
swagger = Swagger(app)

app.url_map.strict_slashes = False

host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """method to handle @app.teardown_appcontext
    """
    storage.close()


if __name__ == "__main__":
    """MAIN"""
    app.run(host=host, port=port, threaded=True)
