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

class ContentHandler(Resource):
    get_and_delete_args = {
        'id': fields.Integer(required=True)      ## id to be retrieved from the carousel GET method
    }
    post_args = {
        'carousel': fields.String(required=True),
        'name': fields.String(required=True),
        'type': fields.String(required=True),
        'location': fields.String(required=True),
        'interval': fields.Integer(required=True),
        'enabled': fields.Bool(required=True)
    }
    put_args = {
        'id': fields.Integer(required=True),
        'carousel': fields.String(),        ## Optional
        'name': fields.String(),            ## Optional
        'type': fields.String(),            ## Optional
        'location': fields.String(),        ## Optional
        'interval': fields.Integer(),       ## Optional
        'enabled': fields.Bool()            ## Optional
    }

    @use_args(get_and_delete_args)
    def get(self, args):
        ## Find the content with the given identifier
        content = Content.query.filter_by(identifier=args['id']).first()
        if content is None:
            abort(404, message="Content item not found")
        ## Serialise the result and return it
        response = {
            "meta": {},
            "links": {
                "self": request.url
            },
            "data": {
                "content": content.serialize
            }
        }
        return jsonify(response)

    @use_args(post_args)
    def post(self, args):
        ## Check the carousel exists
        carousel = Carousel.query.filter_by(name=args['carousel']).first()
        if carousel is None:
            abort(404, message="Carousel not found")
        ## Parse the parameters into mappable data
        contentData = {}
        contentData['name'] = args['name']
        contentData['content_type'] = args['type']
        contentData['content_location'] = args['location']
        contentData['slide_interval'] = args['interval']
        contentData['is_enabled'] = args['enabled']
        ## Create the content instance
        content = Content(**contentData)
        content.carousel_id = carousel.identifier
        ## Insert the Content instance into the database
        db.session.add(content)
        db.session.commit()
        ## Return that the resource has been created
        return "", 201

    @use_args(put_args)
    def put(self, args):
        ## Get the content instance to update
        content = Content.query.filter_by(identifier=args['id'])
        if content.first() is None:
            abort(404, message="Content item not found")
        ## If a carousel was passed, update the content to point to it
        if 'carousel' in args:
            carousel = Carousel.query.filter_by(name=args['carousel']).first()
            if carousel is None:
                abort(404, message="Carousel not found")
            content.first().carousel_id = carousel.identifier
        ## Parse the parameters to a mappable dictionary
        contentData = {}
        if 'name' in args:
            contentData['name'] = args['name']
        if 'type' in args:
            contentData['content_type'] = args['type']
        if 'location' in args:
            contentData['content_location'] = args['location']
        if 'interval' in args:
            contentData['slide_interval'] = args['interval']
        if 'enabled' in args:
            contentData['is_enabled'] = args['enabled']
        ## Check we were given anything to update
        if contentData != {}:
            ## Update the content instance
            content.update(contentData)
        content.first().updated_at = datetime.now()
        content.first().validateContentType()
        db.session.commit()
        return "", 202

    @use_args(get_and_delete_args)
    def delete(self, args):
        ## Find the content with the given identifier
        content = Content.query.filter_by(identifier=args['id']).first()
        if content is None:
            abort(404, message="Content item not found")
        ## Delete the specified content instances
        db.session.delete(content)
        db.session.commit()
        ## Return 202 as the request was executed
        return "", 202
