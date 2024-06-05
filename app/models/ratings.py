from app import db
import pytz
from datetime import datetime

# Model of Ratings table    
class Ratings(db.Model):
    __tablename__ = 'publications'
    
    id = db.Column(db.Integer, primary_key = True)
    rating = db.Column(db.Integer, nullable = False)
    comment = db.Column(db.String(300), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    publication_id = db.Column(db.Integer, db.ForeignKey('publications.id', ondelete='CASCADE'))
    creation_date = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/Warsaw')))
    
    __table_args__ = (
       db.CheckConstraint('rating >= 1 AND rating <= 5', name='rating_range'),
    )
    
    creating_user = db.relationship('Users', backref='comment_creator', lazy=True, foreign_keys='Users.id')
    publication = db.relationship('Publications', backref='publication', lazy=True, foreign_keys='Publications.id')
    
    
    def __init__(self, rating, comment):
        
        self.rating = rating
        self.comment = comment
        