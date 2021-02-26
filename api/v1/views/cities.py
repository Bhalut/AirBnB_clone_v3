#!/usr/bin/python3
<<<<<<< HEAD
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC
from flasgger.utils import swag_from


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
@swag_from('swagger_yaml/cities_by_state.yml', methods=['GET', 'POST'])
def cities_per_state(state_id=None):
    """
        cities route to handle http method for requested cities by state
    """
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        all_cities = storage.all('City')
        state_cities = [obj.to_json() for obj in all_cities.values()
                        if obj.state_id == state_id]
        return jsonify(state_cities)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get("name") is None:
            abort(400, 'Missing name')
        City = CNC.get("City")
        req_json['state_id'] = state_id
        new_object = City(**req_json)
        new_object.save()
        return jsonify(new_object.to_json()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
@swag_from('swagger_yaml/cities_id.yml', methods=['GET', 'DELETE', 'PUT'])
def cities_with_id(city_id=None):
    """
        cities route to handle http methods for given city
    """
    city_obj = storage.get('City', city_id)
    if city_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(city_obj.to_json())

    if request.method == 'DELETE':
        city_obj.delete()
        del city_obj
        return jsonify({}), 200

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        city_obj.bm_update(req_json)
        return jsonify(city_obj.to_json()), 200
=======
""" cities

    cities module RestFull API
"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.city import City
from models.state import State
from models.engine.db_storage import classes


viewer = "State"
specific = "City"
param = "cities"


@app_views.route("/states/<state_id>/cities",
                 methods=["GET"],
                 strict_slashes=False)
def get_cities(state_id):
    """Get cities state

    Args:
        state_id

    Returns:
        response
    """
    state = storage.get(viewer, state_id)
    if state:
        return jsonify([v.to_dict() for v in getattr(state, param)])
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route("/cities/<city_id>",
                 methods=["GET"])
def get_city(city_id):
    """Get city

    Args:
        city_id

    Returns:
        response
    """
    city = storage.get(specific, city_id)
    if city:
        return jsonify(city.to_dict())
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route("/cities/<city_id>",
                 methods=["DELETE"])
def delete_city(city_id):
    """Delete city

    Args:
        city_id

    Returns:
        respose
    """
    city = storage.get(specific, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False,
                 methods=["POST"])
def post_cities(state_id):
    """Post cities in states

    Args:
        state id

    Returns:
        response
    """
    retrieve = request.get_json(force=True, silent=True)
    if retrieve:
        state = storage.get(viewer, state_id)
        if not state:
            return make_response(jsonify({"error": "Not found"}), 404)
        if "name" in retrieve:
            retrieve["state_id"] = state_id
            state = classes[specific](**retrieve)
            state.save()
            return make_response(jsonify(state.to_dict()), 201)
        abort(400, "Missing name")
    abort(400, "Not a JSON")


@app_views.route("/cities/<city_id>",
                 methods=["PUT"])
def put_city(city_id):
    """Put city method

    Args:
        city id

    Returns:
        response
    """
    state = storage.get(specific, city_id)
    if state:
        retrieve = request.get_json(force=True, silent=True)
        if retrieve:
            for k, v in retrieve.items():
                if k not in ["id", "created_at", "updated_at"]:
                    setattr(state, k, v)
            state.save()
            return make_response(jsonify(state.to_dict()), 200)
        abort(400, "Not a JSON")
    return make_response(jsonify({"error": "Not found"}), 404)
>>>>>>> 8397de5d834b17df14283d8f11584ff1dbca1560
