
from flask_sqlalchemy import SQLAlchemy
from config import db



class Ownership(db.Model):
  __tablename__ = 'ownership'
  id = db.Column(db.Integer, primary_key=True)
  owner = db.Column(db.String(), nullable=False)
  unis = db.relationship('Universities', backref ='ownership', lazy=True)

class States(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(), nullable=False)
    unis = db.relationship('Universities', backref ='state', lazy=True)

class Universities(db.Model):
    __tablename__ = 'universities'
    id = db.Column(db.Integer, primary_key=True)
    uni_name = db.Column(db.String(250), nullable = False)
    uni_name_abbr = db.Column(db.String(250), nullable = False)
    vice_chancelor = db.Column(db.String(250), nullable = False)
    vc_image = db.Column(db.String(250), nullable = False)
    uni_image = db.Column(db.String(250), nullable = False)
    uni_images = db.Column(db.ARRAY(db.String()), nullable=True, default=[])
    about_uni = db.Column(db.String(5000), nullable = False)
    location = db.Column(db.String(250), nullable = False)
    uni_website = db.Column(db.String(250), nullable = False)
    nuc_accr_courses = db.Column(db.ARRAY(db.String()), nullable=True, default=[])
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)
    contact_email = db.Column(db.String(250), nullable = True)
    phone_num = db.Column(db.String(), nullable = True)
    date_estb = db.Column(db.String(), nullable = True)
    # date_created = db.Column(db.DateTime, default=datetime.utcnow)
    ownership_id = db.Column(db.Integer, db.ForeignKey('ownership.id'), nullable=False)



# db.create_all()