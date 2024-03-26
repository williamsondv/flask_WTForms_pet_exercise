"""Models for Adopt."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://static-00.iconduck.com/assets.00/paw-icon-512x449-mbgb3633.png"

class Pet(db.Model):

    __tablename__ = "pets"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement = True)
    name = db.Column(db.Text,
                           nullable=False)
    species = db.Column(db.Text,
                           nullable=False)
    img_url = db.Column(db.Text,
                       nullable = False,
                       default = DEFAULT_IMAGE_URL)
    age = db.Column(db.Integer)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, nullable="False",
                          default = True)
    
    @property
    def pet_name(self):
        

        return f"{self.name} {self.species}"
    

   
    

    
    
def connect_db(app):
    with app.app_context():
        db.app = app
        db.init_app(app)
        
    
    

