from app import db
import pytz
from datetime import datetime

# Model of Publications table    
class Publications(db.Model):
    __tablename__ = 'publications'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    description = db.Column(db.String(300), nullable = False)
    price = db.Column(db.Float, nullable = False)
    creating_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    accepting_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable = True)
    creation_date = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/Warsaw')))
    image = db.Column(db.String(100))
    is_visible = db.Column(db.Boolean, default=True)
    
    def __init__(self, name, description, price, creating_user_id, image):\
        
        self.name = name
        self.description = description
        self.price = price
        self.creating_user_id = creating_user_id
        self.image = image
        