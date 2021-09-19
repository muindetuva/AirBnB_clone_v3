#!/usr/bin/python3
""" User view"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route("/users")
def all_users():
    '''Returns a list of all the users'''
    users_list = []
    for user in storage.all("User").values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route("/users/<user_id>")
def user(user_id):
    '''Returns an instance of the specified user'''
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    '''Deletes the specified user'''
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"])
def create_user():
    '''Creates the specified user'''
    if not request.get_json():
        abort(400, description="Not a JSON")

    if not request.get_json().get('email'):
        abort(400, description="Missing email")
    if not request.get_json.get('password'):
        abort(400, description="Missing password")

    user = User()
    user.email = request.get_json()['email']
    user.password = request.get_json()['password']
    user.save()
    #    storage.new(user)
    #    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=['PUT'])
def update_user(user_id):
    '''Updates the user with the id passed'''
    user = storage.get("User", user_id)
    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for k, v in request.get_json().items():
        if k == "id" or k == "created_at" or k == "updated_at" or k == "email":
            continue
        else:
            setattr(user, k, v)

    storage.save()

    return make_response(jsonify(user.to_dict()), 200)
