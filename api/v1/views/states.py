#!/usr/bin/python3
""" States view"""
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage


@app_views.route("/states")
def all_states():
    states_list = []
    for state in storage.all("State").values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route("/states/<state_id>")
def state(state_id):
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


#@app_views.route("/states/<state_id>", methods=['DELETE'])
#def delete_state(state_id):

