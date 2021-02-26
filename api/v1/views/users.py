#!/usr/bin/python3
<<<<<<< HEAD
"""
    Flask route that returns json response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC
from flasgger.utils import swag_from


@app_views.route('/users/', methods=['GET', 'POST'])
@swag_from('swagger_yaml/users_no_id.yml', methods=['GET', 'POST'])
def users_no_id(user_id=None):
    """
        users route that handles http requests with no ID given
    """

    if request.method == 'GET':
        all_users = storage.all('User')
        all_users = [obj.to_json() for obj in all_users.values()]
        return jsonify(all_users)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get('email') is None:
            abort(400, 'Missing email')
        if req_json.get('password') is None:
            abort(400, 'Missing password')
        User = CNC.get('User')
        new_object = User(**req_json)
        new_object.save()
        return jsonify(new_object.to_json()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
@swag_from('swagger_yaml/users_id.yml', methods=['GET', 'DELETE', 'PUT'])
def user_with_id(user_id=None):
    """
        users route that handles http requests with ID given
    """
    user_obj = storage.get('User', user_id)
    if user_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(user_obj.to_json())

    if request.method == 'DELETE':
        user_obj.delete()
        del user_obj
        return jsonify({}), 200

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        user_obj.bm_update(req_json)
        return jsonify(user_obj.to_json()), 200
=======
""" Users

    Users module RestFull API
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users',
                 defaults={'user_id': ''},
                 methods=['GET'],
                 strict_slashes=False)
@app_views.route('/users/<string:user_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_users(user_id):
    """Retrieve an object into a valid JSON

    Args:
        user id

    Returns:
        response
    """
    if user_id != '':
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        return jsonify(user.to_dict())
    else:
        users = [user.to_dict() for user in storage.all(User).values()]
        return jsonify(users)


@app_views.route('/users/<string:user_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a user

    Args:
        user id

    Returns:
        response
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users/',
                 methods=['POST'],
                 strict_slashes=False)
def post_user():
    """Create a user

    Returns:
        response
    """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    required = ["email", "password"]
    for req in required:
        if req not in request.get_json():
            return make_response(jsonify({'error': 'Missing ' + req}), 400)
    user = User(**request.get_json())
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<string:user_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """Update a user

    Args:
        user id

    Returns:
        response
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
>>>>>>> 8397de5d834b17df14283d8f11584ff1dbca1560
