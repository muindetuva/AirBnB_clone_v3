#!/usr/bin/pyhton3
""" init file"""

from flask import Blueprint
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.amenities import *
from api.v1.views.city import *
from api.v1.views.user import *


app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")
