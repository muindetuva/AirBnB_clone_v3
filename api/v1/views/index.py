#!/usr/bin/python3
""" index.py"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status_ok():
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def obj_stats():
    objs = {"amenities": storage.count("Amenities"),
            "cities": storage.count("Cities"),
            "reviews": storage.count("Reviews"),
            "states": storage.count("States"),
            "users": storage.count("Users")}
    print("This is objs {}/n".format(objs))
    return jsonify(objs)
