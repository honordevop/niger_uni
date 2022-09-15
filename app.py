from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:08164462713@localhost:5432/nigeruni'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

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
    about_uni = db.Column(db.String(1000), nullable = False)
    location = db.Column(db.String(250), nullable = False)
    uni_website = db.Column(db.String(250), nullable = False)
    nuc_accr_courses = db.Column(db.ARRAY(db.String()), nullable=True, default=[])
    uni_ownership = db.Column(db.String(250), nullable = False)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)
    contact_email = db.Column(db.String(250), nullable = True)
    phone_num = db.Column(db.String(), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    ownership_id = db.Column(db.Integer, db.ForeignKey('ownership.id'), nullable=False)



# db.create_all()

@app.route('/states')
def get_all_states():
  all_states=[]
  states=States.query.order_by('id').all()

  for state in states:
    all_states.append({
      'State_id': state.id,
      "State": state.state,
    })
  return jsonify(all_states)

@app.route('/states/<state_id>')
def get_universities_list(state_id):
  return render_template('index.html', 
  states=States.query.order_by('id').all(),
  active_state = States.query.get(state_id),
  universities=Universities.query.filter_by(state_id=state_id).order_by('id').all())

@app.route('/ownership/<ownership_id>')
def get_university_owner(ownership_id):
  uni=[]

  ownership = Universities.query.filter_by(ownership_id=ownership_id).order_by('id').all()
  active_owner = Ownership.query.get(ownership_id)

  for university in ownership:
    uni.append({
      "id": university.id,
      "name": university.uni_name,
      'location': university.location,
      'ownership': university.ownership_id,
      'ownership_id': active_owner.owner,
    })

  # return jsonify({
  #               'success': True,
  #               'uni': uni
  #           })


  return render_template('ownership.html', ownership = uni)


@app.route('/')
def index():
  return redirect(url_for('get_universities_list', state_id=1))


#always include this at the bottom of your code
if __name__ == '__main__':
  app.debug=True
  app.run(host="0.0.0.0")