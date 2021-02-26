#!/usr/bin/python3
"""Init views module
"""
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
<<<<<<< HEAD
from api.v1.views.index import *  # noqa
from api.v1.views.states import *  # noqa
from api.v1.views.cities import *  # noqa
from api.v1.views.amenities import *  # noqa
from api.v1.views.users import *  # noqa
from api.v1.views.places import *  # noqa
from api.v1.views.places_reviews import *  # noqa
from api.v1.views.places_amenities import *  # noqa
=======
>>>>>>> 8397de5d834b17df14283d8f11584ff1dbca1560
