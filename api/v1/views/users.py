#!/usr/bin/python3
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
