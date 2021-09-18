#!/usr/bin/python3
""" States view"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route("/states")
def all_states():
    '''Returns a list of all the states'''
    states_list = []
    for state in storage.all("State").values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route("/states/<state_id>")
def state(state_id):
    '''Returns an instance of the specified object'''
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete_state(state_id):
    '''Deletes the specified state'''
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=["POST"])
def create_state():
    '''Creates the specified test'''
    if not request.get_json():
        abort(400, description="Not a JSON")

    if not request.get_json().get('name'):
        abort(400, description="Missing name")

    state = State()
    state.name = request.get_json()['name']
    state.save()
#    storage.new(state)
#    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=['PUT'])
def update_state(state_id):
    '''Updates the state with the id passed'''
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for k, v in request.get_json().items():
        if k == "id" or k == "created_at" or k == "updated_at":
            continue
        else:
            setattr(state, k, v)

    storage.save()

    return make_response(jsonify(state.to_dict()), 200)
