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
    objs = {"amenities": storage.count("Amenity"),
            "cities": storage.count("Citiy"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")}
    return jsonify(objs)
