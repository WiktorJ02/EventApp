from app import db
import pytz
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func
from app.models.ratings import Ratings 

# Model of Publications table    
class Publications(db.Model):
    __tablename__ = 'publications'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    description = db.Column(db.String(300), nullable = False)
    price = db.Column(db.Float, nullable = False)
    localization = db.Column(db.String(30), nullable = False)
    creating_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    creation_date = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/Warsaw')))
    image = db.Column(db.String(100))
    is_visible = db.Column(db.Boolean, default=True)
    
    def __init__(self, name, description, price, localization, image, creating_user_id):
        
        self.name = name
        self.description = description
        self.price = price
        self.localization = localization
        self.image = image
        self.creating_user_id = creating_user_id
    
    def average_rating(self):
        ratings = [rating.rating for rating in self.publication_ratings]
        if ratings:
            return sum(ratings) / len(ratings)
        else:
            return None