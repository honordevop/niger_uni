from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:08164462713@localhost:5432/nigeruni'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

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

# db.create_all()

@app.route('/states/<state_id>')
def get_universities_list(state_id):
  return render_template('index.html', 
  states=States.query.order_by('id').all(),
  active_state = States.query.get(state_id),
  universities=Universities.query.filter_by(state_id=state_id).order_by('id').all())


@app.route('/')
def index():
  return redirect(url_for('get_universities_list', state_id=1))


#always include this at the bottom of your code
if __name__ == '__main__':
  app.debug=True
  app.run(host="0.0.0.0")