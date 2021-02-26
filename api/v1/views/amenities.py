#!/usr/bin/python3
<<<<<<< HEAD
"""
    Flask route that returns json respone
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC
from flasgger.utils import swag_from


@app_views.route('/amenities/', methods=['GET', 'POST'])
@swag_from('swagger_yaml/amenities_no_id.yml', methods=['GET', 'POST'])
def amenities_no_id(amenity_id=None):
    """
        amenities route that handles http requests no ID given
    """
    if request.method == 'GET':
        all_amenities = storage.all('Amenity')
        all_amenities = [obj.to_json() for obj in all_amenities.values()]
        return jsonify(all_amenities)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get('name') is None:
            abort(400, 'Missing name')
        Amenity = CNC.get('Amenity')
        new_object = Amenity(**req_json)
        new_object.save()
        return jsonify(new_object.to_json()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
@swag_from('swagger_yaml/amenities_id.yml', methods=['GET', 'DELETE', 'PUT'])
def amenities_with_id(amenity_id=None):
    """
        amenities route that handles http requests with ID given
    """
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(amenity_obj.to_json())

    if request.method == 'DELETE':
        amenity_obj.delete()
        del amenity_obj
        return jsonify({}), 200

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        amenity_obj.bm_update(req_json)
        return jsonify(amenity_obj.to_json()), 200
=======
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
>>>>>>> 8397de5d834b17df14283d8f11584ff1dbca1560
