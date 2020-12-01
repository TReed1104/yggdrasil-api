from datetime import datetime
from shared import db

class Carousel(db.Model):
    ## The different fields of the model, these generate the table columns
    __tablename__ = 'yggdrasil_carousels'
    identifier = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    name = db.Column(db.String(255), unique=True, nullable=False)
    show_sidebar = db.Column(db.Boolean, unique=False, nullable=False)
    content = db.relationship('Content', back_populates='carousel')

    ## Serialise the model instance ready for jsonification
    @property
    def serialize(self):
        return {
            'id': self.identifier,
            'name': self.name,
            'show_sidebar': self.show_sidebar,
            'content': self.get_content,
            'total_duration': self.get_duration
        }

    ## Serialisation of the content items attached to the carousel
    @property
    def get_content(self):
        if self.content is None:
            return []
        else:
            serialisedContent = []
            for item in self.content:
                serialisedContent.append(item.serialize)
            return serialisedContent

    ## Calculate the sum total duration of the all content items attached to the carousel
    @property
    def get_duration(self):
        if self.content is None:
            return 0
        ## Total up the duration of each carousel content item
        totalDuration = 0
        for contentItem in self.content:
            totalDuration += contentItem.slide_interval
        return totalDuration
