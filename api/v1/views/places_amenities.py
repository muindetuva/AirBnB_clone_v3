#!/usr/bin/python3
""" Amenitys view"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity
from os import getenv


storage_t = getenv("HBNB_TYPE_STORAGE")


@app_views.route("/places/<place_id>/amenities")
def all_place_amenities(place_id):
    '''Returns a list of all the amenities'''

    # Check if place exists
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    amenities_list = []
    if storage_t == "db":
        for amenity in place.amenities:
            amenities_list.append(amenity.to_dict())
    else:
        for amenity in place.amenities:
            amenities_list.append(amenity.to_dict())

    return jsonify(amenities_list)

@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    '''Deletes the specified amenity'''
    # Check if place exists
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    # Check that amenity exists
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    # Check if amenity is linked to place
    if storage_t == "db":
        for amenity in place.amenities:
            if amenity.id == amenity_id:
                # Disconnet the amenity and return
                break
        abort(404)
        
    else:
        if amenity.id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity.id)
        place.save()

    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"])
def create_place_amenity(place_id, amenity_id):
    '''Creates the specified test'''
    # Check if place exists
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    # Check if amenity is linked to place
    if storage_t == "db":
        for amenity in place.amenities:
            if amenity.id == amenity_id:
                return make_response(jsonify(amenity.to_dict()), 200)

        # Connect the amenity and save and return
        return make_response(jsonify(amenity.to_dict()), 201)
        
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)

#        place.amenities = amenity
        setattr(place, amenities, amenity)
#        place.save()
        storage.save()

        return make_response(jsonify(amenity.to_dict()), 201)
