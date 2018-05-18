
# -*- coding: utf-8 -*-
import unittest
from flask_testing import TestCase
from sqlalchemy.exc import IntegrityError
from runtime.utils.class_persistence_template import db
from runtime.rest.app import create_app
from runtime.config.system_config import KEY
from runtime.rest.api import *
from runtime.system.system import System
import datetime
config = {
         'SQLALCHEMY_DATABASE_URI': ''
         }

class TestGetGenericFeedback(TestCase):
    TESTING = True
    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_generic_feedback_form_data(self):
        print "test_get_generic_feedback_form_data"

        headers = {'Content-Type': 'application/json'}
        request_str = "/"

        print "request-str = %s" % request_str
        response = self.client.get(request_str, headers=headers)
        self.assertEqual(response.status_code, 200)

class TestGetGenericLabAndExpFeedback(TestCase):
    TESTING = True
    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_generic_lab_feedback_form_data(self):
        print "test_get_generic_lab_feedback_form_data"

        headers = {'Content-Type': 'application/json'}
        request_str = "/feedback/lab"

        print "request-str = %s" % request_str
        response = self.client.get(request_str, headers=headers)
        self.assertEqual(response.status_code, 200)


    def test_get_generic_exp_feedback_form_data(self):
        print "test_get_generic_exp_feedback_form_data"

        headers = {'Content-Type': 'application/json'}
        request_str = "/feedback/experiment"

        print "request-str = %s" % request_str
        response = self.client.get(request_str, headers=headers)
        self.assertEqual(response.status_code, 200)

class TestAddGenericFeedback(TestCase):
    TESTING = True
    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()
        q_type = "radio"
        question_cls = System.delegate.entities['question']
        question1 = question_cls(name="How is your breakfast?", 
                                  question_type=q_type)
        question2 = question_cls(name="How is your lunch?", 
                                 question_type=q_type)
        question3 = question_cls(name="How is your dinner?", 
                                 question_type=q_type)

        question1.save()
        question2.save()
        question3.save()


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_generic_feedback(self):
        print "test_add_generic_feedback"
        version = "open-edx-virtual-labs-v2.0"
        payload = {'version': version,
            'responses': [{'name': 'How is your breakfast?',
                            'answers':['yes', 'no'] }]
           }

        headers = {'Content-Type': 'application/json'}
        ip_address = {'REMOTE_ADDR': '1.2.3.4'}

        response = self.client.post("/", data=json.dumps(payload),
                                 headers=headers,
                                 environ_overrides=ip_address)

        self.assertEqual(response.status_code, 200)

    def test_add_generic_lab_feedback(self):
        print "test_add_generic_lab_feedback"
        version = "open-edx-virtual-labs-v2.0"

        payload = {'lab_name': 'data structure',
            'version': version,
            'responses': [{'name': 'How is your breakfast?',
                            'answers':['yes', 'no'] }]
           }

        headers = {'Content-Type': 'application/json'}
        ip_address = {'REMOTE_ADDR': '1.2.3.4'}

        response = self.client.post("/", data=json.dumps(payload),
                                 headers=headers,
                                 environ_overrides=ip_address)

        self.assertEqual(response.status_code, 200)

    def test_add_generic_exp_feedback(self):
        print "test_add_generic_exp_feedback"
        version = "open-edx-virtual-labs-v2.0"

        payload = {'lab_name': 'data structure',
            'exp_name': 'tuples',
            'version': version,
            'responses': [{'name': 'How is your breakfast?',
                            'answers':['yes', 'no'] }]
           }

        headers = {'Content-Type': 'application/json'}
        ip_address = {'REMOTE_ADDR': '1.2.3.4'}

        response = self.client.post("/", data=json.dumps(payload),
                                 headers=headers,
                                 environ_overrides=ip_address)

        self.assertEqual(response.status_code, 200)


class TestGetFeedback(TestCase):
    TESTING = True
    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_lab_feedback_form_data(self):
        print "test_get_lab_feedback_form_data"

        lab_name = "Data Structures"
        user_id = "123user"
        version = None
        headers = {'Content-Type': 'application/json'}
        request_str = "/feedback?lab_name=%s&exp_name=%s&user_id=%s&key=%s" \
          % (lab_name, user_id, version, KEY)

        print "request-str = %s" % request_str
        response = self.client.get(request_str, headers=headers)
        self.assertEqual(response.status_code, 200)


    def test_get_exp_feedback_form_data(self):
        print "test_get_exp_feedback_form_data"
        lab_name = "Data Structures"
        exp_name = "binary search"
        user_id = "123user"
        version = None
        headers = {'Content-Type': 'application/json'}
        request_str = "/feedback?lab_name=%s&exp_name=%s&user_id=%s&key=%s \
                      &version=%s"\
                      % (lab_name, exp_name, user_id, version, KEY)

        print "request-str = %s" % request_str
        response = self.client.get(request_str, headers=headers)
        self.assertEqual(response.status_code, 200)

class TestAddFeedback(TestCase):
    TESTING = True
    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()
        q_type = "radio"
        question_cls = System.delegate.entities['question']
        question1 = question_cls(name="How is your breakfast?", 
                                  question_type=q_type)
        question2 = question_cls(name="How is your lunch?", 
                                 question_type=q_type)
        question3 = question_cls(name="How is your dinner?", 
                                 question_type=q_type)

        question1.save()
        question2.save()
        question3.save()


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_exp_feedback(self):
        print "test_add_lab_feedback"
        version = "open-edx-virtual-labs-v2.0"
        payload = {'lab_name': 'data structure',
            'exp_name': 'tuples',
            'key' : KEY,
            'version': version,
            'responses': [{'name': 'How is your breakfast?',
                            'answers':['yes', 'no'] }]
           }

        headers = {'Content-Type': 'application/json'}
        ip_address = {'REMOTE_ADDR': '1.2.3.4'}

        response = self.client.post("/feedback", data=json.dumps(payload),
                                 headers=headers,
                                 environ_overrides=ip_address)

        self.assertEqual(response.status_code, 200)

    def test_add_lab_feedback(self):
        print "test_add_exp_feedback"
        version = "open-edx-virtual-labs-v2.0"
        payload = {'lab_name': 'data structure',
            'key' : KEY,
            'version': version,
            'responses': [{'name': 'How is your breakfast?',
                            'answers':['yes', 'no'] }]
           }

        headers = {'Content-Type': 'application/json'}
        ip_address = {'REMOTE_ADDR': '1.2.3.4'}

        response = self.client.post("/feedback", data=json.dumps(payload),
                                 headers=headers,
                                 environ_overrides=ip_address)

        self.assertEqual(response.status_code, 200)

'''
    def test_get_lab_feedback_form_data(self):
        print "test_get_lab_feedback_form_data"

        headers = {'content-type': 'application/json'}
        response = self.client.get("/feedback?lab_name=data structure&key=some"
                                       " alphanumeric string",
                                        headers=headers)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['lab_name'], "data structure")

    def test_get_exp_feedback_form_data(self):
        print "test_get_exp_feedback_form_data"

        headers = {'content-type': 'application/json'}
        response = self.client.get("/feedback?lab_name=data structure&exp_name"
                                       "=tuples&key=some alphanumeric string",
                                        headers=headers)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['lab_name'], "data structure")
        self.assertEqual(result['exp_name'], "tuples")
'''
class TestGetFeedbackUsage(TestCase):
    TESTING = True
    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()
        q_type = "radio"
        question_cls = System.delegate.entities['question']
        question1 = question_cls(name="How is your breakfast?", 
                                  question_type=q_type)
        question2 = question_cls(name="How is your lunch?", 
                                 question_type=q_type)
        question3 = question_cls(name="How is your dinner?", 
                                 question_type=q_type)

        question1.save()
        question2.save()
        question3.save()


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_feedback_usage(self):
        print "test_get_feedback_usage"

        version = "open-edx-virtual-labs-v2.0"
        payload = {'lab_name': 'data structure',
            'exp_name': 'tuples',
            'key' : KEY,
            'version': version,
            'responses': [{'name': 'How is your breakfast?',
                            'answers':['yes', 'no'] }]
           }

        headers = {'Content-Type': 'application/json'}
        ip_address = {'REMOTE_ADDR': '1.2.3.4'}
        
        response = self.client.post("/feedback", data=json.dumps(payload),
                                 headers=headers,
                                 environ_overrides=ip_address)

        headers = {'content-type': 'application/json'}
        date_obj = datetime.datetime.now().date()
        date_str = date_obj.strftime('%d-%m-%Y')
        url = "/usage_from_feedback?gateway_ip=1.2.3.4&date="+date_str+"&key=defaultkey"
  
        response = self.client.get(url, headers=headers)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 1)
        self.assertEqual(result['usage'], 1)

class TestGetFeedbackDump(TestCase):
    TESTING = True
    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()
        q_type = "radio"
        question_cls = System.delegate.entities['question']
        question1 = question_cls(name="How is your breakfast?", 
                                  question_type=q_type)
        question2 = question_cls(name="How is your lunch?", 
                                 question_type=q_type)
        question3 = question_cls(name="How is your dinner?", 
                                 question_type=q_type)

        question1.save()
        question2.save()
        question3.save()


    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_get_feedback_dump(self):
        print "test_get_feedback_dump"

        version = "open-edx-virtual-labs-v2.0"
        payload = {'lab_name': 'data structure',
            'exp_name': 'tuples',
            'key' : KEY,
            'version': version,
            'responses': [{'name': 'How is your breakfast?',
                            'answers':['yes', 'no'] }]
           }

        headers = {'Content-Type': 'application/json'}
        ip_address = {'REMOTE_ADDR': '1.2.3.4'}
        
        response = self.client.post("/feedback", data=json.dumps(payload),
                                 headers=headers,
                                 environ_overrides=ip_address)

        date_obj = datetime.datetime.now().date()
        date_str = date_obj.strftime('%d-%m-%Y')

        url = "/feedback_dump?date="+date_str+"&key=defaultkey"

        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 200)
#        date_1 = datetime.datetime.strptime(date_str, "%d-%m-%Y").date()
#        print response.data
#        self.assertEqual(response.date, date_1)

class TestAddQuestion(TestCase):
    TESTING = True
    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()
        q_type = "radio"
        question_cls = System.delegate.entities['question']
        question1 = question_cls(name="How is your breakfast?", 
                                  question_type=q_type)
        question2 = question_cls(name="How is your lunch?", 
                                 question_type=q_type)
        question3 = question_cls(name="How is your dinner?", 
                                 question_type=q_type)

        question1.save()
        question2.save()
        question3.save()


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_question(self):
        print "test_question"
        payload = {'name': 'How are you?',
                   'question_type': 'radio',
                   'key': KEY}

        headers = {'Content-Type': 'application/json'}

        response = self.client.post("/questions", data=json.dumps(payload),
                                 headers=headers)

        self.assertEqual(response.status_code, 200)

class TestUpdateQuestion(TestCase):
    TESTING = True
    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()
        q_type = "radio"
        question_cls = System.delegate.entities['question']
        question1 = question_cls(name="How is your breakfast?", 
                                  question_type=q_type)
        question2 = question_cls(name="How is your lunch?", 
                                 question_type=q_type)
        question3 = question_cls(name="How is your dinner?", 
                                 question_type=q_type)

        question1.save()
        question2.save()
        question3.save()


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_update_question(self):
        print "test_update_question"
        payload = {'name': 'How are you?',
                   'question_type': 'radio',
                   'key': KEY}

        payload1 = {'name': 'How are labs?',
                   'question_type': 'text',
                   'key': KEY}

        headers = {'Content-Type': 'application/json'}

        response = self.client.post("/questions", data=json.dumps(payload),
                                 headers=headers)

        response = self.client.put("/questions/1", data=json.dumps(payload1),
                                 headers=headers)

        self.assertEqual(response.status_code, 200)

class TestDeleteQuestion(TestCase):
    TESTING = True
    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()
        q_type = "radio"
        question_cls = System.delegate.entities['question']
        question1 = question_cls(name="How is your breakfast?", 
                                  question_type=q_type)
        question2 = question_cls(name="How is your lunch?", 
                                 question_type=q_type)
        question3 = question_cls(name="How is your dinner?", 
                                 question_type=q_type)

        question1.save()
        question2.save()
        question3.save()


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_delete_question(self):
        print "test_delete_question"

        payload = {'name': 'How are you?',
                   'question_type': 'radio',
                   'key': KEY
                  }

        headers = {'Content-Type': 'application/json'}

        response = self.client.post("/questions", data=json.dumps(payload),
                                 headers=headers)

        response = self.client.delete("/questions/1", headers=headers)

        self.assertEqual(response.status_code, 200)

class TestGetQuestion(TestCase):
    TESTING = True
    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()
        q_type = "radio"
        question_cls = System.delegate.entities['question']
        question1 = question_cls(name="How is your breakfast?", 
                                  question_type=q_type)
        question2 = question_cls(name="How is your lunch?", 
                                 question_type=q_type)
        question3 = question_cls(name="How is your dinner?", 
                                 question_type=q_type)

        question1.save()
        question2.save()
        question3.save()


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_questions(self):
        print "test_question"
        payload = {'name': 'How are you?',
                   'question_type': 'radio',
                   'key': KEY}

        headers = {'Content-Type': 'application/json'}

        response = self.client.post("/questions", data=json.dumps(payload),
                                 headers=headers)

        response = self.client.get("/questions", headers=headers)
        self.assertEqual(response.status_code, 200)

class TestFeedbackDumpToElk(TestCase):
     TESTING = True
     def create_app(self):
	 app = create_app(config)
	 return app

     def setUp(self):
	 db.create_all()

     def tearDown(self):
	 db.session.remove()
	 db.drop_all()

     def test_feedback_details_to_elk_aws_cloud(self):
	 print "test_dump_feedback_details_to_elk_aws_cloud"
	 payload = {
	     'key' : KEY,
	     'feedbacks': [
		 {
		     "user_id": "Null",
		     "responses": [
			 {
			     "question": {
				 "name": "Please provide any other feedback about Virtual Labs",
				 "question_type": "textarea",
				 "id": 21
			     },
			     "answers": [
				 {
				     "name": "test",
				     "id": 18
				 }
			     ],
			     "id": 40
			 },
			 {
			     "question": {
				 "name": "Designation",
				 "question_type": "radio",
				 "id": 22
			     },
			     "answers": [
				 {
				     "name": "Student",
				     "id": 1
				 }
			     ],
			     "id": 1
			 },
			 {
			     "question": {
				 "name": "Did you attempt any experiments ?",
				 "question_type": "radio",
				 "id": 23
			     },
			     "answers": [
				 {
				     "name": "No",
				     "id": 2
				 }
			     ],
			     "id": 10
			 },
			 {
			     "question": {
				 "name": "Please rate your experience",
				 "question_type": "radio",
				 "id": 24
			     },
			     "answers": [
				 {
				     "name": "2/10",
				     "id": 4
				 }
			     ],
			     "id": 11
			 }
		     ],
		     "exp_name": "Null",
		     "lab_name": "generic feedback",
		     "version": "generic-feedback-v2.0",
		     "gateway_ip": "10.100.1.7",
		     "date": "21-10-2016",
		     "id": 14
		 }
	     ]
	 }

     def test_feedback_details_to_elk_college_cloud(self):
	 print "test_dump_feedback_details_to_elk_college_cloud"
	 payload = {
	     'key' : KEY,
	     'feedbacks': [
		 {
		     "user_id": "Null",
		     "responses": [
			 {
			     "question": {
				 "name": "Please provide any other feedback about Virtual Labs",
				 "question_type": "textarea",
				 "id": 21
			     },
			     "answers": [
				 {
				     "name": "test",
				     "id": 18
				 }
			     ],
			     "id": 40
			 },
			 {
			     "question": {
				 "name": "Designation",
				 "question_type": "radio",
				 "id": 22
			     },
			     "answers": [
				 {
				     "name": "Student",
				     "id": 1
				 }
			     ],
			     "id": 1
			 },
			 {
			     "question": {
				 "name": "Did you attempt any experiments ?",
				 "question_type": "radio",
				 "id": 23
			     },
			     "answers": [
				 {
				     "name": "No",
				     "id": 2
				 }
			     ],
			     "id": 10
			 },
			 {
			     "question": {
				 "name": "Please rate your experience",
				 "question_type": "radio",
				 "id": 24
			     },
			     "answers": [
				 {
				     "name": "2/10",
				     "id": 4
				 }
			     ],
			     "id": 11
			 }
		     ],
		     "exp_name": "Null",
		     "lab_name": "generic feedback",
		     "version": "generic-feedback-v2.0",
		     "gateway_ip": "10.100.1.7",
		     "date": "21-10-2016",
		     "id": 14
		 }
	     ]
	 }

	 headers = {'Content-Type': 'application/json'}

	 response = self.client.post("/dump_feedback_to_elastic_db", data=json.dumps(payload),
				  headers=headers)

	 self.assertEqual(response.status_code, 200)
   
class TestDumpCollegeDetailsToElk(TestCase):
   TESTING = True
   def create_app(self):
       app = create_app(config)
       return app

   def setUp(self):
       db.create_all()

   def tearDown(self):
       db.session.remove()
       db.drop_all()

   def test_dump_college_details_to_elk(self):
       print "test_dump_college_details_to_elk"
       payload = {
	    'key' : KEY,
	    'college_details':{ 
		 "college_address":"hyd", 
		 "college_name": "bhoj reddy", 
		 "college_pincode":"500080", 
		 "contact_name":"madhavi", 
		 "contact_no":"9866188505", 
		 "email_id":"madhavi@vlabs.ac.in",
		 "mac_addr":"44:a8:42:f1:df:ef" }
       }

       headers = {'Content-Type': 'application/json'}

       response = self.client.post("/dump_cc_details_to_elastic_db", \
				   data=json.dumps(payload), headers=headers)

       self.assertEqual(response.status_code, 200)
     
class TestDumpUsageDetailsToElk(TestCase):
      TESTING = True
      def create_app(self):
	  app = create_app(config)
	  return app

      def setUp(self):
	  db.create_all()

      def tearDown(self):
	  db.session.remove()
	  db.drop_all()

      def test_dump_usage_details_to_elk(self):
	  print "test_dump_usage_details_to_elk"
	  payload = {
	      'key' : KEY,
              'mac_addr': "44:a8:42:f1:df:ef",
	      'usages' : [
		  {
		      "LAB_ID": "CSE19",
		      "DATE_OF_EXPERIMENT": "2017-01-04",
		      "STUDENT_ID": "106ecd878f4148a5cabb6bbb0979b730",
		      "REGION": "anonymous",
		      "LAB_NAME": "Image Processing Lab",
		      "EXPERIMENT_NAME": "Distance and Connectivity",
		      "EXPERIMENT_ID": "E99751",
		      "TIME_OF_EXPERIMENT": "16:38",
		      "IP_ADDRESS": "10.100.1.7"
		  }
	      ]
	  }

	  headers = {'Content-Type': 'application/json'}

	  response = self.client.post("/dump_usage_to_elastic_db", data=json.dumps(payload),
				   headers=headers)

	  self.assertEqual(response.status_code, 200)
      
class TestFeedbackDumpToElk(TestCase):
     TESTING = True
     def create_app(self):
	 app = create_app(config)
	 return app

     def setUp(self):
	 db.create_all()

     def tearDown(self):
	 db.session.remove()
	 db.drop_all()

     def test_feedback_details_to_elk_aws_cloud(self):
	 print "test_dump_feedback_details_to_elk_aws_cloud"
	 payload = {
	     'key' : KEY,
	     'feedbacks': [
		 {
		     "user_id": "Null",
		     "responses": [
			 {
			     "question": {
				 "name": "Please provide any other feedback about Virtual Labs",
				 "question_type": "textarea",
				 "id": 21
			     },
			     "answers": [
				 {
				     "name": "test",
				     "id": 18
				 }
			     ],
			     "id": 40
			 },
			 {
			     "question": {
				 "name": "Designation",
				 "question_type": "radio",
				 "id": 22
			     },
			     "answers": [
				 {
				     "name": "Student",
				     "id": 1
				 }
			     ],
			     "id": 1
			 },
			 {
			     "question": {
				 "name": "Did you attempt any experiments ?",
				 "question_type": "radio",
				 "id": 23
			     },
			     "answers": [
				 {
				     "name": "No",
				     "id": 2
				 }
			     ],
			     "id": 10
			 },
			 {
			     "question": {
				 "name": "Please rate your experience",
				 "question_type": "radio",
				 "id": 24
			     },
			     "answers": [
				 {
				     "name": "2/10",
				     "id": 4
				 }
			     ],
			     "id": 11
			 }
		     ],
		     "exp_name": "Null",
		     "lab_name": "generic feedback",
		     "version": "generic-feedback-v2.0",
		     "gateway_ip": "10.100.1.7",
		     "date": "21-10-2016",
		     "id": 14
		 }
	     ]
	 }

     def test_feedback_details_to_elk_college_cloud(self):
	 print "test_dump_feedback_details_to_elk_college_cloud"
	 payload = {
	     'key' : KEY,
	     'feedbacks': [
		 {
		     "user_id": "Null",
		     "responses": [
			 {
			     "question": {
				 "name": "Please provide any other feedback about Virtual Labs",
				 "question_type": "textarea",
				 "id": 21
			     },
			     "answers": [
				 {
				     "name": "test",
				     "id": 18
				 }
			     ],
			     "id": 40
			 },
			 {
			     "question": {
				 "name": "Designation",
				 "question_type": "radio",
				 "id": 22
			     },
			     "answers": [
				 {
				     "name": "Student",
				     "id": 1
				 }
			     ],
			     "id": 1
			 },
			 {
			     "question": {
				 "name": "Did you attempt any experiments ?",
				 "question_type": "radio",
				 "id": 23
			     },
			     "answers": [
				 {
				     "name": "No",
				     "id": 2
				 }
			     ],
			     "id": 10
			 },
			 {
			     "question": {
				 "name": "Please rate your experience",
				 "question_type": "radio",
				 "id": 24
			     },
			     "answers": [
				 {
				     "name": "2/10",
				     "id": 4
				 }
			     ],
			     "id": 11
			 }
		     ],
		     "exp_name": "Null",
		     "lab_name": "generic feedback",
		     "version": "generic-feedback-v2.0",
		     "gateway_ip": "10.100.1.7",
		     "date": "21-10-2016",
		     "id": 14
		 }
	     ]
	 }

	 headers = {'Content-Type': 'application/json'}

	 response = self.client.post("/dump_feedback_to_elastic_db", data=json.dumps(payload),
				  headers=headers)

	 self.assertEqual(response.status_code, 200)
   
if __name__ == '__main__':
    unittest.main()
