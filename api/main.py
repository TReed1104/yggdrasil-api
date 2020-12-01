## Imports
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from models import carousel, content
from shared import db
from resources import list_carousels, list_content
from resources import handler_carousel, handler_content

## Create our Flask app and connect it to our database
app = Flask(__name__)
api = Api(app)
app.config.from_pyfile('configs/main.cfg')
CORS(app)
db.init_app(app)
with app.app_context():
    db.create_all()

## Register the resources and the endpoints to access them
api.add_resource(list_carousels.CarouselList, '/carousels')
api.add_resource(list_content.ContentList, '/carouselcontent')
api.add_resource(handler_carousel.CarouselHandler, '/carousel_handler')
api.add_resource(handler_content.ContentHandler, '/content_handler')

if __name__ == '__main__':
    ## Initialise the application, 0.0.0.0 means to use our machine ip and enable debugging if needed
    app.run(host='0.0.0.0', port='5000')
