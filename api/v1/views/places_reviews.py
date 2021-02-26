#!/usr/bin/python3
<<<<<<< HEAD
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from flasgger.utils import swag_from
from models import storage, CNC


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
@swag_from('swagger_yaml/reviews_by_place.yml', methods=['GET', 'POST'])
def reviews_per_place(place_id=None):
    """
        reviews route to handle http method for requested reviews by place
    """
    place_obj = storage.get('Place', place_id)

    if request.method == 'GET':
        if place_obj is None:
            abort(404, 'Not found')
        all_reviews = storage.all('Review')
        place_reviews = [obj.to_json() for obj in all_reviews.values()
                         if obj.place_id == place_id]
        return jsonify(place_reviews)

    if request.method == 'POST':
        if place_obj is None:
            abort(404, 'Not found')
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        user_id = req_json.get("user_id")
        if user_id is None:
            abort(400, 'Missing user_id')
        user_obj = storage.get('User', user_id)
        if user_obj is None:
            abort(404, 'Not found')
        if req_json.get('text') is None:
            abort(400, 'Missing text')
        Review = CNC.get("Review")
        req_json['place_id'] = place_id
        new_object = Review(**req_json)
        new_object.save()
        return jsonify(new_object.to_json()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
@swag_from('swagger_yaml/reviews_id.yml', methods=['GET', 'DELETE', 'PUT'])
def reviews_with_id(review_id=None):
    """
        reviews route to handle http methods for given review by ID
    """
    review_obj = storage.get('Review', review_id)

    if request.method == 'GET':
        if review_obj is None:
            abort(404, 'Not found')
        return jsonify(review_obj.to_json())

    if request.method == 'DELETE':
        if review_obj is None:
            abort(404, 'Not found')
        review_obj.delete()
        del review_obj
        return jsonify({}), 200

    if request.method == 'PUT':
        if review_obj is None:
            abort(404, 'Not found')
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        review_obj.bm_update(req_json)
        return jsonify(review_obj.to_json()), 200
=======
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
>>>>>>> 8397de5d834b17df14283d8f11584ff1dbca1560
