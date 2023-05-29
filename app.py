import sys
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, session
from config import app
from model import Universities,Ownership,States
from datetime import datetime
from helperFxn import get_university_by_ownership, search_institution_by_abbr, fetchAllUniversities, fetch_single_university, institutionListByState


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


"""@app.route('/states/<id>')
def get_state_university_list(id):
  universities = get_universities_list_by_state(id)
  return render_template('institutions.html', data = universities)"""

@app.route('/ownership/private/')
def privateUniversities():
  # universities = get_university_by_ownership(1, Universities)
  universities = Universities.query.filter_by(ownership_id=1)

  page = request.args.get('page')
  print(page)

  if page and page.isdigit():
    page = int(page)
  else:
    page = 1

  pages = universities.paginate(page, per_page=5)
  return render_template('institutions.html', data = universities, pages=pages)
  

@app.route('/ownership/state/')
def stateUniversities():
  # universities = get_university_by_ownership(2, Universities)
  universities = Universities.query.filter_by(ownership_id=2)

  page = request.args.get('page')
  print(page)

  if page and page.isdigit():
    page = int(page)
  else:
    page = 1

  pages = universities.paginate(page, per_page=5)
  return render_template('institutions.html', data = universities, pages=pages)
   

@app.route('/ownership/federal/')
def federalUniversities():
  # universities = get_university_by_ownership(3, Universities)
  universities = Universities.query.filter_by(ownership_id=3)

  page = request.args.get('page')
  print(page)

  if page and page.isdigit():
    page = int(page)
  else:
    page = request.args.get('page', 1, type=int)

  pages = universities.paginate(page, per_page=5)
  # return jsonify({
  #   "data": uni,
  #   "pages": pages.items
  # })
  return render_template('institutions.html', data = universities, pages=pages)


#   # return jsonify({
#   #               'success': True,
#   #               'uni': uni
#   #           })

#   return render_template('ownership.html', ownership = uni)




@app.route('/institutions/search/', methods=['GET'])
def search_university_by_abbr():
  universities = search_institution_by_abbr()
  if universities:
    return render_template('searchResult.html', data = universities)
  else:
    return render_template('notFound.html', error='Not found')

@app.route('/universities/')
def fetch_all_universities():
  alluniversities = fetchAllUniversities()
  
  return render_template('institutions.html', data = alluniversities)

@app.route('/university/search')
def search_a_university():
  universities = search_institution_by_abbr()
  print(universities)
  if universities:
    return render_template('searchResult.html', data = universities)
  else:
    return render_template('notFound.html', error='Not found')
  # return university
  # return render_template('institution.html', uni = university)

# fetch single University
@app.route('/university/<uni_name>')
def fetch_a_university_details(uni_name):
  university = fetch_single_university(uni_name)
  # return jsonify(university)
  if (university):
    return render_template('institution.html', uni=university[0])
  else:
    return render_template('notFound.html', error='Not found')


@app.route('/universities/search/', methods=['GET'])
def search_universities_by_state():
  statename = request.args.get('state')
  session["statename"] = statename
  if not statename:
      statename = session.get("statename")

      
      
  if statename:
    stateSearched = States.query.filter(States.state.ilike("%" + statename + "%")).first()
  # result = institutionListByState()
    if stateSearched:
      universities = Universities.query.filter_by(state_id=stateSearched.id)
  else:
    return render_template('notFound.html', error='Not found')
  
  page = request.args.get('page')

  if page and page.isdigit():
    page = int(page)
  else:
    page = 1

  pages = universities.paginate(page, per_page=5)

  return render_template('institutions.html', data = universities, pages=pages, route="/universities/search/")

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
  count = Universities.query.count()
  return render_template('index.html', count = count)
  # return redirect(url_for('get_universities_list'))

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found ooo"
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