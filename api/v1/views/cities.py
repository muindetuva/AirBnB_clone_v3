#!/usr/bin/python3
""" Cities app view"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage

from models.city import City


@app_views.route("/states/<state_id>/cities")
def all_cities(state_id):
    '''Returns a list of all the cities'''
    # Check that the state_id actually exists
    if not storage.get("State", state_id):
        abort(404)

    cities_list =[]
    cities = storage.get("State", state_id).cities
    for city in cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)

#    cities_list = []
#    for state in storage.all("State").values():
#        if state.id == state_id:
#            pass
#        else:
#            abort(400)
#    for city in storage.all("City").values():
#        if city.state_id == state_id:
#            cities_list.append(city.to_dict())
#    return jsonify(cities_list)


@app_views.route("/cities/<city_id>")
def city(city_id):
    '''Returns an instance of the specified city'''
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def delete_city(city_id):
    '''Deletes the specified city'''
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    '''Creates the specified city'''

    # Check that the state with that id exists
    if not storage.get("State", state_id):
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if not request.get_json().get('name'):
        abort(400, description="Missing name")

    city = City()
    city.name = request.get_json().get('name')
    city.state_id = state_id
    city.save()
    return make_response(jsonify(city.to_dict()), 201)

#    all_state_ids = []
#    for state in storage.all("State").values():
#        all_state_ids.append(state.id)

#    if state_id in all_state_ids:
#        city = City()
#        city.name = request.get_json()['name']
#        city.state_id = state_id
#        city.save()
        #    storage.new(city)
        #    storage.save()
#    else:
#        abort(404)

#    return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=['PUT'])
def update_city(city_id):
    '''Updates the city with the id passed'''
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for k, v in request.get_json().items():
        if k == "id" or k == "created_at" or k == "updated_at" \
           or k == "state_id":
            continue
        else:
            setattr(city, k, v)

    storage.save()

    return make_response(jsonify(city.to_dict()), 200)
