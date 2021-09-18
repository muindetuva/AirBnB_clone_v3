#!/usr/bin/python3
""" States view"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/states/")
def all_states():
    states_list = []
    for state in storage.all("State").values():
        states_list.append(state.to_dict())
    return jsonify(states_list)
