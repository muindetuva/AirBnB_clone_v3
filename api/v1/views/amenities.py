#!/usr/bin/python3
""" Amenitys view"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities")
def all_amenities():
    '''Returns a list of all the amenities'''
    amenities_list = []
    for amenity in storage.all("Amenity").values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>")
def amenity(amenity_id):
    '''Returns an instance of the specified object'''
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'])
def delete_amenity(amenity_id):
    '''Deletes the specified amenity'''
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"])
def create_amenity():
    '''Creates the specified test'''
    if not request.get_json():
        abort(400, description="Not a JSON")

    if not request.get_json().get('name'):
        abort(400, description="Missing name")

    amenity = Amenity()
    amenity.name = request.get_json()['name']
    amenity.save()
#    storage.new(amenity)
#    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=['PUT'])
def update_amenity(amenity_id):
    '''Updates the amenity with the id passed'''
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for k, v in request.get_json().items():
        if k == "id" or k == "created_at" or k == "updated_at":
            continue
        else:
            setattr(amenity, k, v)

    storage.save()

    return make_response(jsonify(amenity.to_dict()), 200)
