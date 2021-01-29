#!/usr/bin/python3
""" Places

    Places handler for all default RestFul API
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<string:city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieve all places from a City

    Args:
        city id

    Returns:
        response
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_by_city = [v.to_dict() for v in storage.all(
        Place).values() if v.city_id == city_id]
    return jsonify(places_by_city)


@app_views.route('/places/<string:place_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieve a Place by ID

    Args:
        place id

    Returns:
        response
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place

    Args:
        place id

    Returns:
        response
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<string:city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Create a place

    Args:
        city id

    Returns:
        response
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    update_dict = request.get_json()
    user = storage.get(User, update_dict['user_id'])
    if user is None:
        abort(404)
    if 'name' not in update_dict:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    update_dict['city_id'] = city_id
    place = Place(**update_dict)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<string:place_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Update a place

    Args:
        place id

    Returns:
        response
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)
