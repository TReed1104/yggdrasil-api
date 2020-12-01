## Imports
from datetime import datetime
from flask import request
from flask_restful import Resource, abort
from flask_jsonpify import jsonify
from webargs import fields
from webargs.flaskparser import use_args
from shared import db
from models.carousel import Carousel

class CarouselHandler(Resource):
    get_args = {
        'id': fields.Integer(),
        'name': fields.String()
    }
    delete_args = {
        'id': fields.Integer(required=True)
    }
    post_args = {
        'name': fields.String(required=True),
        'show_sidebar': fields.Bool(required=True)
    }
    put_args = {
        'id': fields.Integer(required=True),
        'show_sidebar': fields.Bool(required=True),
        'new_name': fields.String()     # Optional
    }

    @use_args(get_args)
    def get(self, args):
        ## Default value the carousel to catch mistakes
        carousel = None
        if "id" in args:
            ## get the carousel with the supplied id
            carousel = Carousel.query.filter_by(identifier=args['id']).first()
        elif "name" in args:
            ## get the carousel with the supplied name
            carousel = Carousel.query.filter_by(name=args['name']).first()
        else:
            ## Abort as neither the name or id are present
            abort(422, message="Invalid Parameters")
        ## Check we found a carousel
        if carousel is None:
            abort(404, message="Carousel not found")
        ## Serialise the carousel and return it
        response = {
            "meta": {},
            "links": {
                "self": request.url
            },
            "data": {
                "carousel": carousel.serialize
            }
        }
        return jsonify(response)

    @use_args(post_args)
    def post(self, args):
        ## Check the carousel doesn't already exist
        doesCarouselExist = Carousel.query.filter_by(name=args['name']).first()
        if doesCarouselExist is not None:
            abort(422, message="A carousel already exists with the supplied name")
        ## Convert the data to a valid dictionary
        carouselData = {}
        carouselData['name'] = args['name']
        carouselData['show_sidebar'] = args['show_sidebar']
        ## Create the Carousel
        carousel = Carousel(**carouselData)
        ## Push the data to the database
        db.session.add(carousel)
        db.session.commit()
        ## Return that the resource has been created
        return "", 201

    @use_args(put_args)
    def put(self, args):
        ## Check the carousel doesn't already exist
        carousel = Carousel.query.filter_by(identifier=args['id'])
        if carousel.first() is None:
            abort(404, message="Carousel not found")
        ## Parse the parameters to a unpackable dictionary
        carouselData = {}
        carouselData['show_sidebar'] = args['show_sidebar']
        ## If a new name has been specified
        if 'new_name' in args:
            ## Check if a carousel with the new name exists
            doesNewCarouselExist = Carousel.query.filter_by(name=args['new_name']).first()
            if doesNewCarouselExist is not None:
                abort(422, message="A carousel already exists with the new name")
            ## Set the name of the carousel to the new name
            carouselData['name'] = args['new_name']
        ## Update the carousel
        carousel.first().updated_at = datetime.now()
        carousel.update(carouselData)
        db.session.commit()
        ## Return that the resource has been updated
        return "", 202

    @use_args(delete_args)
    def delete(self, args):
        ## get the carousel with the supplied name
        carousel = Carousel.query.filter_by(identifier=args['id']).first()
        ## Check we found a carousel
        if carousel is None:
            abort(404, message="Carousel not found")
        ## Delete the chosen carousel
        db.session.delete(carousel)
        db.session.commit()
        ## Return 202 as the request was executed
        return "", 202
