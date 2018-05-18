
# -*- coding: utf-8 -*-
import os
import requests
import json
from flask import session, render_template, Blueprint, request, \
     jsonify, abort, current_app, redirect, url_for
from flask import Flask
from runtime.utils.type_utils import jsonify_list
from runtime.config.system_config import KEY
from runtime.exceptions.custom_exceptions import *
from runtime.system.system_interface import SystemInterface
from runtime.config.flask_app_config import GENERIC_FEEDBACK_VERSION,\
     GENERIC_LAB_FEEDBACK_VERSION, GENERIC_EXP_FEEDBACK_VERSION, ELASTIC_DB_URL, FOOTER_URL

import yaml

api = Blueprint('APIs', __name__)

def post_data_to_elastic_search(index_name, doc_name, record):                                                                                          
    try:
        FEEDBACK_ELASTIC_DB_URL = "%s/%s/%s" % (ELASTIC_DB_URL, index_name, doc_name)                                                                                                                                                
        current_app.logger.debug("FEEDBACK_ELASTIC_DB_URL : %s" % (FEEDBACK_ELASTIC_DB_URL))                                           
        resp = requests.post(FEEDBACK_ELASTIC_DB_URL, data=json.dumps(record))                                                                               
        if not resp.status_code == 201:                                                                                                                 
            current_app.logger.debug("Error_code : %s" % (resp.status_code))                                                                            
            return False                                                                                                                                
        else:                                                                                                                                           
            current_app.logger.debug("Status_code : %s" % (resp.status_code))                                                                           
            return True                                                                                                                                 
    except Exception as e:                                                                                                                              
        print str(e)
        return False

@api.route('/', methods=['GET', 'POST'])
def get_generic_feedback():
    if request.method == 'GET':
        current_app.logger.debug("get generic feedback")
        response = SystemInterface.get_generic_feedback_form\
          (GENERIC_FEEDBACK_VERSION)
        return render_template('index.html', 
                            questions_data=response, footer_url=FOOTER_URL)
    if request.method == 'POST':
        current_app.logger.debug("generic feedback post")
        if request.is_json:
            data_json = json.dumps(request.get_json())
            data_dict = yaml.safe_load(data_json)
        else:
            abort(500, "the request does not contain data in json")

        try:
            gateway_ip = str(request.access_route[-1])
            data_dict["gateway_ip"] = gateway_ip
            current_app.logger.debug("execute add_generic_feedback")
            fb = SystemInterface.add_generic_feedback(data_dict)
            current_app.logger.debug("exectued add_generic_feedback")
            return jsonify('{"status":"sucess"}')

        except TypeError as err:
            error_message = 'Malformed arguments, error: %s' % str(err)
            current_app.logger.error("%s" %(error_message))
            return render_template('error.html', 
                    data=error_message)

        except Exception as err:
            current_app.logger.error("Exception : %s" %(err))
            abort(500, 'error: %s' % str(err))
            
@api.route('/feedback/<string>', methods=['GET'])
def get_add_generic_lab_and_exp_feedback(string):
    if request.method == 'GET':
        if string == 'lab':
            current_app.logger.debug("execute get_generic_feedback_form")
            response = SystemInterface.get_generic_feedback_form\
              (GENERIC_LAB_FEEDBACK_VERSION)
            current_app.logger.debug("executed get_generic_feedback_form")
            return render_template('index.html', 
                                questions_data=response, footer_url=FOOTER_URL)
        elif string == 'experiment':
            current_app.logger.debug("execute get_generic_feedback_form")
            response = SystemInterface.get_generic_feedback_form\
              (GENERIC_EXP_FEEDBACK_VERSION)
            current_app.logger.debug("executed get_generic_feedback_form")
            return render_template('index.html', 
                                questions_data=response, footer_url=FOOTER_URL)

    if request.method == 'POST':
        if request.is_json:
            data_json = json.dumps(request.get_json())
            data_dict = yaml.safe_load(data_json)
        else:
            abort(500, "the request does not contain data in json")

        try:
            gateway_ip = str(request.access_route[-1])
            data_dict["gateway_ip"] = gateway_ip
            current_app.logger.debug("execute add_generic_lab_and_exp_feedback")
            fb = SystemInterface.add_generic_lab_and_exp_feedback(data_dict)
            current_app.logger.debug("executed add_generic_lab_and_exp_feedback")
            return jsonify('{"status":"sucess"}')

        except TypeError as err:
            error_message = 'Malformed arguments, error: %s' % str(err)
            current_app.logger.error("%s" %(error_message))
            return render_template('error.html', 
                    data=error_message)

        except Exception as err:
            current_app.logger.error("%s" %(error_message))
            abort(500, 'error: %s' % str(err))

@api.route('/success', methods=['GET'])
def get_success_template():
    current_app.logger.debug("")
    return render_template('success.html')

@api.route('/feedback', methods=['GET', 'POST'])
def get_add_feedback():
    if request.method == 'GET':
        current_app.logger.debug("")
        if 'lab_name' not in request.args or 'key' not in request.args:
            error_message = 'Either lab_name or key or both arguments are not passed'
            return render_template('error.html', data=error_message)
        else:
            lab_name = str(request.args['lab_name'])
            key = str(request.args['key'])

        if 'exp_name' not in request.args:
            exp_name = None
        else:
            exp_name = str(request.args['exp_name'])

        if 'date' not in request.args:
            date = None
        else:
            date = str(request.args['date'])

        if 'version' not in request.args:
            version = None
        else:
            version = str(request.args['version'])

        if 'user_id' not in request.args:
            user_id = None
        else:
            user_id = str(request.args['user_id'])
            current_app.logger.debug("lab_name = %s, exp_name=%s, user_id=%s, "
                        "key=%s" % (lab_name, exp_name, user_id, key))
        try:
            current_app.logger.debug("execute get_feedback_form")
            response = SystemInterface.get_feedback_form(key, 
                                lab_name, 
                                exp_name,
                                version,
                                user_id)
            current_app.logger.debug("executed get_feedback_form")                            
            return render_template('index.html', 
                    questions_data=response, footer_url=FOOTER_URL)

        except NotAuthorizedError as err:
            error_message = 'Not Authorized error: %s' % str(err)
            current_app.logger.error("%s" %(error_message))
            return render_template('error.html', 
                    data=error_message)
            
        except TypeError as err:
            error_message = 'Malformed arguments, error: %s' % str(err)
            current_app.logger.error("%s" %(error_message))
            return render_template('error.html', 
                    data=error_message)
        except Exception as err:
            error_message = 'error: %s' % str(err)
            current_app.logger.error("%s" %(error_message))
            return render_template('error.html', 
                    data=error_message)

    if request.method == 'POST':
        if request.is_json:
            data_json = json.dumps(request.get_json())
            data_dict = yaml.safe_load(data_json)
        else:
            abort(500, "the request does not contain data in json")

        if 'lab_name' not in data_dict or 'key' not in data_dict or \
           'responses' not in data_dict or 'version' not in data_dict:
            abort(400, 'Either lab name or key or version or responses' 
                      ' are not passed')
        else:
            gateway_ip = str(request.access_route[-1]) 
            current_app.logger.debug("lab_name = %s, responses=%s, "
                                         "version=%s, key=%s, "
                          %(data_dict['lab_name'], data_dict['responses'],
                            data_dict['version'], data_dict['key']))

            data_dict["gateway_ip"] = gateway_ip
        try:
            current_app.logger.debug("execute add_feedback")
            fb = SystemInterface.add_feedback(data_dict)
            current_app.logger.debug("execute add_feedback")
            return jsonify('{"status":"sucess"}')

        except NotAuthorizedError as err:
            current_app.logger.error("%s" %(err))
            abort(401, 'Not Authorized error: %s' % str(err))
        except TypeError as err:
            current_app.logger.error("%s" %(err))
            abort(400, 'Malformed arguments, error: %s' % str(err))
        except Exception as err:
            current_app.logger.error("%s" %(err))
            abort(500, 'error: %s' % str(err))
  
@api.route('/usage_from_feedback', methods=['GET'])
def get_feedback_usage():
    if request.method == 'GET':
        if 'gateway_ip' in request.args and 'date' in request.args and 'key'\
            in request.args:
            gateway_ip = str(request.args['gateway_ip'])
            date  = request.args['date']
            key = request.args['key']
            try:
                current_app.logger.debug("execute get_feedback_usage")
                usage_count = SystemInterface.get_feedback_usage(gateway_ip,\
                                                                 date, key)
                current_app.logger.debug("executed get_feedback_usage")
                usage = {'usage': usage_count}
                return jsonify(usage)
            except NotAuthorizedError as err:
                error_message =  'Not Authorized error: %s' % str(err)
                """
                if request.headers['Content-Type'] == "application/json":
                    abort(401, error_message)
                else:
                """
                current_app.logger.error("%s" %(error_message))
                return render_template('error.html', 
                                       data=error_message)
            except TypeError as err:
                error_message = 'Malformed arguments, error: %s' % str(err)
                """
                if request.headers['Content-Type'] == "application/json":
                abort(400, error_message)
                else:
                """
                current_app.logger.error("%s" %(error_message))
                return render_template('error.html', 
                                       data=error_message)
            except Exception as err:
                error_message = 'error: %s' % str(err)
                """
                if request.headers['Content-Type'] == "application/json":
                abort(400, error_message)
                else:
                """
                current_app.logger.error("%s" %(error_message))
                return render_template('error.html', 
                                    data=error_message)

            
@api.route('/feedback_dump', methods=['GET', 'POST'])
def get_feedback_dump():
    if request.method == 'GET':
        if 'date' in request.args and 'key' in request.args:
            date  = request.args['date']
            key = request.args['key']
            
            try:
                current_app.logger.debug("execute get_feedback_dump")
                feedbacks = SystemInterface.get_feedback_dump(date, key)
                current_app.logger.debug("executed get_feedback_dump")
                return jsonify_list(feedbacks)
                
            except NotAuthorizedError as err:
                error_message =  'Not Authorized error: %s' % str(err)                
                current_app.logger.error("%s" %(error_message))
                abort(401, error_message)

            except TypeError as err:
                error_message = 'Malformed arguments, error: %s' % str(err)
                current_app.logger.error("%s" %(error_message))
                abort(400, error_message)                

            except Exception as err:
                error_message = 'error: %s' % str(err)
                current_app.logger.error("%s" %(error_message))
                abort(404, error_message)
                
            

@api.route('/get_gateway_ip', methods=['GET'])
def get_gateway_ip():
    try:
        current_app.logger.debug("")
        gateway_ip = str(request.access_route[-1])
        return jsonify({'gateway_ip': gateway_ip}) 
    except Exception as e:
        current_app.logger.error("%s" %(str(e)))
        return "Error in getting the gateway_ip"
  
@api.route('/questions', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        try:
            current_app.logger.debug("execute get_questions")
            questions = SystemInterface.get_questions()
            current_app.logger.debug("executed get_questions")

            return jsonify_list(questions)

        except TypeError as err:
            error_message = 'Malformed arguments, error: %s' % str(err)
            current_app.logger.error("%s" %(error_message))
            return render_template('error.html', 
                    data=error_message)

        except Exception as err:
            current_app.logger.error("%s" %(err))
            abort(500, 'error: %s' % str(err))
       
    if request.method == 'POST':
        if request.is_json:
            data_json = json.dumps(request.get_json())
            data_dict = yaml.safe_load(data_json)
        else:
            abort(500, "the request does not contain data in json")

        try:
            current_app.logger.debug("execute add_question")
            q1 = SystemInterface.add_question(data_dict)
            current_app.logger.debug("executed add_question")
            return jsonify(q1)

        except TypeError as err:
            error_message = 'Malformed arguments, error: %s' % str(err)
            current_app.logger.error("%s" %(err))
            return render_template('error.html', 
                    data=error_message)

        except Exception as err:
            current_app.logger.error("%s" %(err))
            abort(500, 'error: %s' % str(err))
            
@api.route('/questions/<id>', methods=['GET', 'PUT', 'DELETE'])
def update_and_delete_question(id):
    if request.method == 'GET':
        try:
            current_app.logger.debug("execute get_question_by_id(id)")
            question = SystemInterface.get_question_by_id(id)
            current_app.logger.debug("executed get_question_by_id(id)")
            return jsonify(question)

        except NotFoundError as err:
            error_message = "No question found with id: %s found." % id
            current_app.logger.error("%s" %(error_message))
            return render_template('error.html',
                    data=error_message)

        except TypeError as err:
            error_message = 'Malformed arguments, error: %s' % str(err)
            current_app.logger.error("%s" %(error_message))
            return render_template('error.html', 
                    data=error_message)

        except Exception as err:
            current_app.logger.error("%s" %(err))
            abort(500, 'error: %s' % str(err))
    
    if request.method == 'PUT':
        if request.is_json:
            data_json = json.dumps(request.get_json())
            data_dict = yaml.safe_load(data_json)
            data_dict['q_id']=id
        else:
            abort(500, "the request does not contain data in json")

        try:
            current_app.logger.debug("execute update_question")
            q1 = SystemInterface.update_question(data_dict)
            current_app.logger.debug("execute update_question")
            return jsonify(q1)

        except TypeError as err:
            error_message = 'Malformed arguments, error: %s' % str(err)
            current_app.logger.error("%s" %(err))
            return render_template('error.html', 
                    data=error_message)

        except Exception as err:
            current_app.logger.error("%s" %(err))
            abort(500, 'error: %s' % str(err))

    if request.method == 'DELETE':

        try:
            
            current_app.logger.debug("execute delete_question")
            q1 = SystemInterface.delete_question(id)
            current_app.logger.debug("executed delete_question")
            return jsonify('{"status":"sucess"}')

        except TypeError as err:
            error_message = 'Malformed arguments, error: %s' % str(err)
            current_app.logger.error("%s" %(error_message))
            return render_template('error.html', 
                    data=error_message)

        except Exception as err:
            current_app.logger.error("%s" %(err))
            abort(500, 'error: %s' % str(err))



@api.route('/dump_feedback_to_elastic_db', methods=['GET', 'POST'])
def dump_feedback_to_elk():

    if request.method == 'GET':
	return "Method not allowed"

    if request.method == 'POST':
	data_json = json.dumps(request.get_json())
	data_dict = yaml.safe_load(data_json)

	if 'feedbacks' not in data_dict or 'key' not in data_dict:
	    abort(400, 'feedbacks or key attribute is not passed')

        if data_dict['key'] != KEY:
	    abort(401, 'Unauthorized to perform this operation')
	
	feedbacks = data_dict['feedbacks']
	key = data_dict['key']        
        doc_name = "feedback"

	if 'mac_addr' in data_dict:
	    mac_addr = str(data_dict['mac_addr'])
            cc_details_elastic_db_url = "%s/college_cloud/details/id=%s" % (ELASTIC_DB_URL, mac_addr)
            current_app.logger.debug("college cloud elastic db url : %s " % (cc_details_elastic_db_url))
	    r = requests.get(cc_details_elastic_db_url)
	    if r.json()['found'] == False:		
		return jsonify({"status" : "failed", "error" : "College cloud is not registered"})
	    else:
		current_app.logger.debug("College Cloud Details : %s " % (r.json()))
		index_name = str(r.json()['_source']['college_name']) + "_" + str(mac_addr) 
		current_app.logger.debug("index_name : %s, doc_name : %s " % (index_name, doc_name))
	else:
	    index_name = "vlabs"
            current_app.logger.debug("Elastic Search URL : %s " % (ELASTIC_DB_URL))
	    current_app.logger.debug("index_name : %s, doc_name : %s " % (index_name, doc_name))

	for feedback in feedbacks:
	    if(post_data_to_elastic_search(index_name, doc_name, feedback)):
		current_app.logger.debug("Added Feedback : %s " % (feedback))
	    else:
		current_app.logger.error("failed to add feedback: %s " % (feedback))
		abort(500)

	return jsonify({"status" : "success"})
                  
@api.route('/dump_cc_details_to_elastic_db', methods=['GET', 'POST'])
def dump_cc_details_to_elk():
  if request.method == 'GET':
      return "Method not allowed"

  if request.method == 'POST':
      try:
	  data_json = json.dumps(request.get_json())
	  data_dict = yaml.safe_load(data_json)

	  if 'college_details' not in data_dict or 'key' not in data_dict:
	      abort(400, 'college_details or key attribute is not passed')

          if data_dict['key'] != KEY:
	      abort(401, 'Unauthorized to perform this operation')


	  if 'key' not in data_dict:
	      print "Unauthorized to perform this operation"
	      abort(401, 'Unauthorized to perform this operation')

	  cc_details = data_dict['college_details']
	  key = data_dict['key']

	  current_app.logger.debug("College Data : %s " % (cc_details))
	  mac_addr = cc_details['mac_addr']            
	  cc_details_elastic_db_url = "%s/college_cloud/details/id=%s" \
				      % (ELASTIC_DB_URL, str(mac_addr))

	  current_app.logger.debug("college cloud elastic db url : %s " \
				   % (cc_details_elastic_db_url))
	  college_data = requests.get(cc_details_elastic_db_url)

          if college_data.status_code == 404:
	      create_college = requests.post(cc_details_elastic_db_url,
					     data=json.dumps(cc_details))

	      if create_college.status_code == 200 or create_college.status_code == 201:
		  current_app.logger.debug("Added college details : %s "
				       % (cc_details))
		  return jsonify({"status" : "success"})
	      else:
		  current_app.logger.debug("Error in adding college details : %s " % (cc_details))
		  abort(int(college_data.status_code),
			"{'status' : 'Error in adding college details'}")
	  else:
	      current_app.logger.debug("College details already exists : %s "
				       % (cc_details))
	      return jsonify({"status" : "College details already present"})
      except Exception as e:
	  abort(500, str(e))
@api.route('/dump_usage_to_elastic_db', methods=['GET', 'POST'])
def dump_usage_to_elk():
    if request.method == 'GET':
	return "Method not allowed"
    if request.method == 'POST':
	data_json = json.dumps(request.get_json())
	data_dict = yaml.safe_load(data_json)

	if 'usages' not in data_dict or 'mac_addr' not in data_dict or 'key' not in data_dict:
	    abort(400, 'usages attribute or mac_addr or key attribute is not passed')

        if data_dict['key'] != KEY:
	    abort(401, 'Unauthorized to perform this operation')

	usages = data_dict['usages']
	mac_addr = data_dict['mac_addr']
	key = data_dict['key']
        mac_addr = str(data_dict['mac_addr'])
        cc_details_elastic_db_url = "%s/college_cloud/details/id=%s" % (ELASTIC_DB_URL, mac_addr)
        current_app.logger.debug("college cloud elastic db url : %s " % (cc_details_elastic_db_url))
	
	try:
            r = requests.get(cc_details_elastic_db_url)	    
	    if r.json()['found'] == False:
		current_app.logger.debug("ELASTIC DB URL : %s " % (ELASTIC_DB_URL))
		return jsonify({"status" : "failed", "error" : "College cloud is not registered"})
	    else:
		current_app.logger.debug("College Cloud Details : %s " % (r.json()))
                college_name = str(r.json()['_source']['college_name'])
		index_name = college_name + "_" + str(mac_addr)
		doc_name = "usages"
		current_app.logger.debug("index_name : %s, doc_name: %s " \
                                     % (index_name, doc_name))

		for usage in usages:
		    if(post_data_to_elastic_search(index_name, doc_name, usage['_source'])):
			current_app.logger.debug("Added usage : %s " % (usage['_source']))
		    else:
			current_app.logger.error("failed to add usage: %s " % (usage['_source']))
			abort(500)

		return jsonify({"status" : "success"})
	except Exception as e:
	    abort(500, str(e))
