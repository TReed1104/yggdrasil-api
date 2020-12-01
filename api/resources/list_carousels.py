## Imports
from datetime import datetime
from flask import request
from flask_restful import Resource
from flask_jsonpify import jsonify
from shared import db
from models.carousel import Carousel

class CarouselList(Resource):
    def get(self):
        ## Get all the carousels registered with Yggdrasil
        carousels = Carousel.query.all()
        carouselsResponseArray = []
        if carousels is not None:
            carouselsResponseArray = [carousel.serialize for carousel in carousels]
        ## generate our JSON response
        response = {
            "meta": {},
            "links": {
                "self": request.url
            },
            "data": {
                "carousels": carouselsResponseArray
            }
        }
        return jsonify(response)
