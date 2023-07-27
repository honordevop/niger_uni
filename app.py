import sys
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from config import app
from model import Universities,Ownership,States
from datetime import datetime
import random
from flask_cors import CORS
from helperFxn import get_university_by_ownership, search_institution_by_abbr, fetchAllUniversities, fetch_single_university, institutionListByState, fetchTopChoiceUniversity


cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/states/')
def get_all_states():
  all_states=[]
  states=States.query.order_by('id').all()

  for state in states:
    all_states.append({
      'State_id': state.id,
      "State": state.state,
    })
  return jsonify({
    'count': len(all_states),
    'data': all_states
  }),200


@app.route('/university/create', methods=['POST'])
def create_uni():
  error = False
  body = {}
  try:
    uni_name = request.get_json()['uniName']
    uni_name_abbr = request.get_json()['nameAbbr']
    vice_chancelor = request.get_json()['viceChancellor']
    vc_image = request.get_json()['vcImage']
    uni_image = request.get_json()['uniImage']
    about_uni = request.get_json()['aboutUni']
    location = request.get_json()['loCation']
    uni_website = request.get_json()['uniWebsite']
    contact_email = request.get_json()['contactEmail']
    phone_num = request.get_json()['phoneNum']
    nuc_accr_courses = request.get_json()['nucAccrCourses']
    ownership_id = request.get_json()['uniOwnership']
    state_id = request.get_json()['state_id']
    university = Universities(
      uni_name=uni_name, 
      uni_name_abbr=uni_name_abbr,
      vice_chancelor=vice_chancelor,
      vc_image=vc_image,
      uni_image=uni_image,
      uni_website=uni_website,
      about_uni=about_uni,
      location=location,
      nuc_accr_courses=nuc_accr_courses,
      state_id=state_id,
      contact_email=contact_email,
      phone_num=phone_num,
      ownership_id=ownership_id, 
    )
    db.session.add(university)
    db.session.commit()
    body['id'] = university.id
    body['completed'] = university.uni_name
    body['description'] = university.location
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify(body)


@app.route('/universities/ownership/private/')
def privateUniversities():
  try:
    universities = get_university_by_ownership(1, Universities)
  except:
    abort(400)
  sliced = 20
  data = random.sample(universities, sliced)
  return jsonify({
    'count': len(data),
    'status': 200,
    'data': data,
  }), 200

@app.route('/universities/ownership/state/')
def stateUniversities():
  try:
    universities = get_university_by_ownership(2, Universities)
  except:
    abort(400)
  sliced = 20
  data = random.sample(universities, sliced)
  return jsonify({
    'count': len(data),
    'status': 200,
    'data': data,
  }), 200
  

@app.route('/universities/ownership/federal/')
def federalUniversities():
  try:
    universities = get_university_by_ownership(3, Universities)
  except:
    abort(400)
  sliced = 20
  data = random.sample(universities, sliced)
  return jsonify({
    'count': len(data),
    'status': 200,
    'data': data,
  }), 200



@app.route('/university/search', methods=['GET'])
def search_university_by_abbr():
  try:
    universities = search_institution_by_abbr()
  except:
    abort(400)
  if universities:
    data = universities[0:20]
    return jsonify({
      'count': len(data),
      'status': 200,
      'data': data,
    }), 200
  elif universities==None:
    abort(404)
  else:
    abort(400)

@app.route('/universities/')
def fetch_all_universities():
  try:
    universities = fetchAllUniversities()
  except:
    abort(400)
  sliced = 20
  data = random.sample(universities, sliced)
  if data:
    return jsonify({
      'count': len(data),
      'status': 200,
      'data': data,
    }), 200
  elif data==None:
    abort(404)
  else:
    abort(400)

    
@app.route('/university/<int:id>')
def fetch_a_university_details(id):
  try:
    universities = fetch_single_university(id)
  except:
    abort(400)
  # return jsonify(university)
  
  if (universities):
    data = universities
    return jsonify({
      'count': len(data),
      'status': 200,
      'data': data,
    }), 200
  elif universities==None:
    abort(404)
  else:
    abort(400)


@app.route('/universities/search', methods=['GET'])
def search_universities_by_state():
  try:
    result = institutionListByState()
  except:
    abort(400)
  if (result):
    data = result[0:20]
    return jsonify({
      'count': len(data),
      'status': 200,
      'data': data,
    }), 200
  elif result==None:
    abort(404)
  else:
    abort(400)
  # if result:
  #   return render_template('institutions.html', data = result)
  # else:
  #   return render_template('notFound.html', error='Not found')

@app.route('/universities/topchoice/')
def TopUniversities():
  try:
    universities = fetchTopChoiceUniversity()
  except:
    abort(400)
  data = universities
  return jsonify({
    'count': len(data),
    'status': 200,
    'data': data,
  }), 200

@app.route('/admin/', defaults={'state_id': 1})
@app.route('/admin/<state_id>')
def admin_page(state_id):
  return render_template('adminHome.html', 
  states=States.query.order_by('id').all(),
  active_state = States.query.get(state_id),
  universities=Universities.query.filter_by(state_id=state_id).order_by('id').all())


@app.route('/footer')
def footer():
  return render_template('footer.html')


@app.route('/')
def index():
  return render_template('index.html')
  # return redirect(url_for('get_universities_list'))

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

def unprocessable(error):
  return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
  }), 422

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(405)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405

#always include this at the bottom of your code
if __name__ == '__main__':
  app.debug=True
  app.run(host="0.0.0.0")