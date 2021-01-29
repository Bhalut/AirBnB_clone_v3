#!/usr/bin/python3
""" Places Reviews

    Places Reviews module RestFull API
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieve all reviews from a Place

    Args:
        place id

    Returns:
        response
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews_by_place = [v.to_dict() for v in storage.all(
        Review).values() if v.place_id == place_id]
    return jsonify(reviews_by_place)


@app_views.route('/reviews/<string:review_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieve a Review by ID

    Args:
        review id

    Returns:
        response
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review

    Args:
        review id

    Returns:
        response
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Create a review

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
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    update_dict = request.get_json()
    user = storage.get(User, update_dict['user_id'])
    if user is None:
        abort(404)
    if 'text' not in update_dict:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    update_dict['place_id'] = place_id
    review = Review(**update_dict)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """Update a review

    Args:
        review id

    Returns:
        response
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
