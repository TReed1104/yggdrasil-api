## Imports
from datetime import datetime
from flask import request
from flask_restful import Resource, abort
from flask_jsonpify import jsonify
from webargs import fields
from webargs.flaskparser import use_args
from shared import db
from models.carousel import Carousel
from models.content import Content

class ContentList(Resource):
    get_args = {
        'carousel': fields.String()
    }

    @use_args(get_args)
    def get(self, args):
        if 'carousel' in args:
            ## Get the content linked to a specified carousel
            carousel = Carousel.query.filter_by(name=args['carousel']).first()
            if carousel is None:
                abort(404, message='Carousel not found')
            contents = Content.query.all()
            contentArray = []
            ## Check we found any content
            if contents is not None:
                ## Find the content linked to the chosen carousel
                for content in contents:
                    if content.carousel is not None:
                        if content.carousel.name == args['carousel']:
                            contentArray.append(content.serialize)
            ## Generate our response
            response = {
                "meta": {},
                "links": {
                    "self": request.url
                },
                "data": {
                    "carousel_content": contentArray
                }
            }
            return jsonify(response)
        else:
            ## Serialise all the content registered with the system
            contents = Content.query.all()
            contentsResponseArray = []
            if contents is not None:
                contentsResponseArray = [content.serialize for content in contents]
            ## Generate our JSON response
            response = {
                "meta": {},
                "links": {
                    "self": request.url
                },
                "data": {
                    "carousel_content": contentsResponseArray
                }
            }
            return jsonify(response)
