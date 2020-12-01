from datetime import datetime
from shared import db

class Content(db.Model):
    ## The different fields of the model, these generate the table columns
    __tablename__ = 'yggdrasil_content'
    identifier = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    name = db.Column(db.String(255), unique=False, nullable=False)
    carousel_id = db.Column(db.Integer, db.ForeignKey("yggdrasil_carousels.identifier"))
    carousel = db.relationship('Carousel', back_populates="content")
    content_type = db.Column(db.String(255), unique=False, nullable=False)
    content_location = db.Column(db.String(255), unique=False, nullable=False)
    slide_interval = db.Column(db.Integer, unique=False, nullable=False)            # in milliseconds
    is_enabled = db.Column(db.Boolean, unique=False, nullable=False, default=True)

    def __init__(self, **kwargs):
        ## Default constructor handling by SQLAlchemy ORM
        super(Content, self).__init__(**kwargs)

        ## Custom constructor code
        self.validateContentType()

    ## Serialise the model instance ready for jsonification
    @property
    def serialize(self):
        return {
            'id': self.identifier,
            'name': self.name,
            'carousel': self.carousel_name,
            'carousel_id': self.carousel_id,
            'type': self.content_type,
            'location': self.content_location,
            'interval': self.slide_interval,
            'is_enabled': self.is_enabled
        }

    ## Function for grabbing the name of the carousel this content item is attached to
    @property
    def carousel_name(self):
        if self.carousel is not None:
            if self.carousel.name is not None:
                return self.carousel.name
        return "Not Set"

    def validateContentType(self):
        validTypes = ['picture', 'video', 'webpage', 'heimdall', 'mimir']
        if self.content_type not in validTypes:
            self.content_type = 'invalid'
