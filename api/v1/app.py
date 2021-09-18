#!/usr/bin/python3
""" Creates an flask web service"""

from flask import Flask
import os

app = Flask(__name__)

from models import storage
from api.v1.views import app_views

app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(self):
    """ removes the current SQLAlchemy session"""
    storage.close()

if __name__ == "__main__":
    if os.getenv("HBNB_API_HOST") and os.getenv("HBNB_API_PORT"):
        app.run(host=os.getenv("HBNB_API_HOST"),
                port=os.getenv("HBNB_API_PORT"), threaded=True)
    else:
        app.run(host='0.0.0.0', port=5000, threaded=True)
