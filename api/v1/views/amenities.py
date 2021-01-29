#!/usr/bin/python3
""" Amenities

    Amenities module RestFull API
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', defaults={'amenity_id': ''},
                 methods=['GET'],
                 strict_slashes=False)
@app_views.route('/amenities/<string:amenity_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_amenities(amenity_id):
    """Retrieve an amenitie object into a valid JSON

    Args:
        amenity id

    Returns:
        response
    """
    if amenity_id != '':
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        return jsonify(amenity.to_dict())
    else:
        amenities = [amenity.to_dict()
                     for amenity in storage.all(Amenity).values()]
        return jsonify(amenities)


@app_views.route('amenities/<string:amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete a amenity

    Args:
        amenity id

    Returns:
        response
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities/',
                 methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """Create a amenity

    Returns:
        response
    """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    amenity = Amenity(**request.get_json())
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Update a amenity

    Args:
        amenity id

    Returns:
        response
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
