#!/usr/bin/python3
<<<<<<< HEAD
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from flasgger.utils import swag_from
from models import storage, CNC
from os import environ
STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')


@swag_from('swagger_yaml/places_by_city.yml', methods=['GET', 'POST'])
@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def places_per_city(city_id=None):
    """
        places route to handle http method for requested places by city
    """
    city_obj = storage.get('City', city_id)
    if city_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        all_places = storage.all('Place')
        city_places = [obj.to_json() for obj in all_places.values()
                       if obj.city_id == city_id]
        return jsonify(city_places)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        user_id = req_json.get("user_id")
        if user_id is None:
            abort(400, 'Missing user_id')
        user_obj = storage.get('User', user_id)
        if user_obj is None:
            abort(404, 'Not found')
        if req_json.get("name") is None:
            abort(400, 'Missing name')
        Place = CNC.get("Place")
        req_json['city_id'] = city_id
        new_object = Place(**req_json)
        new_object.save()
        return jsonify(new_object.to_json()), 201


@swag_from('swagger_yaml/places_id.yml', methods=['GET', 'DELETE', 'PUT'])
@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def places_with_id(place_id=None):
    """
        places route to handle http methods for given place
    """
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(place_obj.to_json())

    if request.method == 'DELETE':
        place_obj.delete()
        del place_obj
        return jsonify({}), 200

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        place_obj.bm_update(req_json)
        return jsonify(place_obj.to_json()), 200


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """
        places route to handle http method for request to search places
    """
    all_places = [p for p in storage.all('Place').values()]
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    states = req_json.get('states')
    if states and len(states) > 0:
        all_cities = storage.all('City')
        state_cities = set([city.id for city in all_cities.values()
                            if city.state_id in states])
    else:
        state_cities = set()
    cities = req_json.get('cities')
    if cities and len(cities) > 0:
        cities = set([
            c_id for c_id in cities if storage.get('City', c_id)])
        state_cities = state_cities.union(cities)
    amenities = req_json.get('amenities')
    if len(state_cities) > 0:
        all_places = [p for p in all_places if p.city_id in state_cities]
    elif amenities is None or len(amenities) == 0:
        result = [place.to_json() for place in all_places]
        return jsonify(result)
    places_amenities = []
    if amenities and len(amenities) > 0:
        amenities = set([
            a_id for a_id in amenities if storage.get('Amenity', a_id)])
        for p in all_places:
            p_amenities = None
            if STORAGE_TYPE == 'db' and p.amenities:
                p_amenities = [a.id for a in p.amenities]
            elif len(p.amenities) > 0:
                p_amenities = p.amenities
            if p_amenities and all([a in p_amenities for a in amenities]):
                places_amenities.append(p)
    else:
        places_amenities = all_places
    result = [place.to_json() for place in places_amenities]
    return jsonify(result)
=======
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
>>>>>>> 8397de5d834b17df14283d8f11584ff1dbca1560
