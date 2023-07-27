import sys
from model import Universities,Ownership,States
from flask import render_template, request, abort
from sqlalchemy import or_


def institutionListFxn(universities, id=''):
  institutionList=[]

  for university in universities:
    ownerName = Ownership.query.get(university.ownership_id)
    institutionList.append({
      "id": university.id,
      "name": university.uni_name,
      'location': university.location,
      # 'ownership': university.ownership_id,
      'ownership': ownerName.owner,
      "about": university.about_uni,
      "uni_name_abbr": university.uni_name_abbr,
      "contact_email": university.contact_email,
      "vc_image": university.vc_image,
      "vice_chancelor": university.vice_chancelor,
      "uni_image": university.uni_image,
      "uni_images": university.uni_images,
      "uni_website": university.uni_website,
      "phone_num": university.phone_num,
    })

  return institutionList

def single_intitution_format(instutionData):
  instution = {
      "id": instutionData.id,
      "name": instutionData.uni_name,
      'location': instutionData.location,
      'ownership': instutionData.ownership_id,
      'owner': Ownership.query.get(instutionData.ownership_id).owner,
      "about": instutionData.about_uni,
      "uni_name_abbr": instutionData.uni_name_abbr,
      "contact_email": instutionData.contact_email,
      "vc_image": instutionData.vc_image,
      "vice_chancelor": instutionData.vice_chancelor,
      "uni_images": instutionData.uni_images,
      "uni_website": instutionData.uni_website,
      "phone_num": instutionData.phone_num,
  }

  return instution

def institutionListByState():   #State_Id
  statename = request.args.get('state')
  stateSearched = States.query.filter(States.state.ilike("%" + statename + "%")).all()
  if stateSearched:
    for state in stateSearched:
      universities=Universities.query.filter_by(state_id=state.id).order_by('id').all()
      institutionLists = institutionListFxn(universities)
    return institutionLists

def get_university_by_ownership(id, institutionType):  #ownership_id
  print(institutionType)
  universities = institutionType.query.filter_by(ownership_id=id).order_by('id').all()

  institutionLists = institutionListFxn(universities, id)
  # return jsonify({
  #               'success': True,
  #               'uni': uni
  #           })

  return institutionLists

"""def get_universities_list_by_state(state_id):
  # print(state_id)
  universities = institutionListByState(state_id)
  return universities"""


def search_institution_by_abbr():
  abbre = request.args.get('name')  
  uni_abbre_result = Universities.query.filter(Universities.uni_name_abbr.ilike("%" + abbre + "%")).all()
  uni_name_result = Universities.query.filter(Universities.uni_name.ilike("%" + abbre + "%")).all()

  if (uni_abbre_result):
    universities = uni_abbre_result
  # if (universities2):
  elif (uni_name_result):
    universities = uni_name_result
  else:
    return
  try:
    institutionLists = institutionListFxn(universities)
    return institutionLists
  except:
    abort(404)
  # return render_template('institutions.html', data = uni)



def fetchAllUniversities():
  universities = Universities.query.order_by('id').all()
  alluniversities = institutionListFxn(universities)
  return alluniversities

def fetch_single_university(id):
  university = Universities.query.filter_by(id=id)  
  university_details = institutionListFxn(university)
  return university_details

def fetchTopChoiceUniversity():
  ids = ['6', '26', '32', '33', '35', '37', '38', '126']

  sample = []
  for id in ids:
    topChoice = Universities.query.filter(Universities.id.in_([id])).all()
    for res in topChoice:
      location = res.location.split(",")      
      sample.append({
      'id': res.id,
      'uni_name': res.uni_name,
      'location': location[0],
      'state': location[1],
      'image': res.uni_image
      
    })
  # result = session.query(Customers).filter(or_(Customers.id>2, Customers.name.like('Ra%')))
  # print(sample)
  if (sample):
    return sample
  # if (universities2):
  else:
    abort(404)


