#!/usr/bin/python3
""" Reviews view"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews")
def all_reviews(place_id):
    '''Returns a list of all the reviews'''

    # Check if place exists
    if not storage.get("Place", place_id):
        abort(404)

    reviews_list = []
    for review in storage.all("Review").values():
        if review.place_id == place_id:
            reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route("/reviews/<review_id>")
def review(review_id):
    '''Returns an instance of the specified object'''
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'])
def delete_review(review_id):
    '''Deletes the specified review'''
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    '''Creates the specified test'''
    # Check if place exists
    if not storage.get("Place", place_id):
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    user_id = request.get_json().get('user_id')
    if not user_id:
        abort(400, description="Missing user_id")

    if not storage.get("User", user_id):
        abort(404)

    if not request.get_json().get('text'):
        abort(400, description="Missing text")

    review = Review()
    review.text = request.get_json()['text']
    review.place_id = place_id
    review.user_id = user_id
    review.save()
#    storage.new(review)
#    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=['PUT'])
def update_review(review_id):
    '''Updates the review with the id passed'''
    review = storage.get("Review", review_id)
    if not review:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for k, v in request.get_json().items():
        if k == "id" or k == "created_at" or k == "updated_at" \
           or k == "user_id" or k == "place_id":
            continue
        else:
            setattr(review, k, v)

    storage.save()

    return make_response(jsonify(review.to_dict()), 200)
