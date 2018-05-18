
# -*- coding: utf-8 -*-
import unittest
from flask_testing import TestCase
from runtime.rest.app import create_app
from sqlalchemy.exc import IntegrityError
from runtime.utils.class_persistence_template import db
from runtime.system.system_interface import *
from runtime.config.system_config import KEY
from flask import current_app
config = {
         'SQLALCHEMY_DATABASE_URI': ''
         }

class TestGetFeedbackForm(TestCase):
    TESTING = True
    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_feedback_form_in_system_interface(self):
        print "test_get_feedback_form_in_system_interface"

        lab_name = "data structures"
        exp_name = "binary search"
        user_id = "123user"
        version = None
        key = KEY

        questions_dict = SystemInterface.get_feedback_form(key, lab_name, 
                                                               exp_name,
                                                               version,
                                                               user_id)
                                                               
        self.assertEqual(questions_dict['lab_name'], lab_name)

    def test_get_feedback_form_with_type_error(self):
        print "test_get_feedback_form_with_type_error"

        lab_name = None
        exp_name = "binary search"
        user_id = "123user"
        key = KEY

        with self.assertRaises(TypeError):
            SystemInterface.get_feedback_form(key, 
                                              lab_name, 
                                              exp_name,
                                              user_id)

    def test_get_feedback_form_with_auth_error(self):
        print "test_get_feedback_form_with_auth_error"

        lab_name = "Data Structures"
        exp_name = "binary search"
        user_id = "123user"
        version = None
        key = "temp"

        with self.assertRaises(NotAuthorizedError):
            SystemInterface.get_feedback_form(key, 
                                              lab_name, 
                                              exp_name,
                                              version,
                                              user_id)

class TestGetFeedbackForm(TestCase):
    TESTING = True
    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_feedback_form_in_system_interface(self):
        print "test_get_feedback_form_in_system_interface"

        lab_name = "data structures"
        exp_name = "binary search"
        user_id = "123user"
        version = None
        key = KEY

        questions_dict = SystemInterface.get_feedback_form(key, lab_name, 
                                                               exp_name,
                                                               version,
                                                               user_id)
                                                               
        self.assertEqual(questions_dict['lab_name'], lab_name)

    def test_get_feedback_form_with_type_error(self):
        print "test_get_feedback_form_with_type_error"

        lab_name = None
        exp_name = "binary search"
        user_id = "123user"
        key = KEY

        with self.assertRaises(TypeError):
            SystemInterface.get_feedback_form(key, 
                                              lab_name, 
                                              exp_name,
                                              user_id)

    def test_get_feedback_form_with_auth_error(self):
        print "test_get_feedback_form_with_auth_error"

        lab_name = "Data Structures"
        exp_name = "binary search"
        user_id = "123user"
        version = None
        key = "temp"

        with self.assertRaises(NotAuthorizedError):
            SystemInterface.get_feedback_form(key, 
                                              lab_name, 
                                              exp_name,
                                              version,
                                              user_id)

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

    def test_add_feedback_in_system_interface(self):
        print "test_add_feedback_in_system_interface"

        version = "open-edx-virtual-labs-v2.0"
        user_id = "John123"
        data_dict = {'lab_name': 'data structure',
                    'exp_name': 'tuples',
                    'key' : KEY,
                    'gateway_ip': '10.4.12.24',
                    'version': version,
                    'user_id': user_id,
                    'responses': [{'name': 'How is your breakfast?',
                                    'answers':['yes', 'no'] }]
                   }

        fb = SystemInterface.add_feedback(data_dict)
        feedback_cls = System.delegate.entities['feedback']
        fb = feedback_cls.get_all()[0]
        
        self.assertEqual(fb.get("lab_name"), data_dict['lab_name'])
        self.assertEqual(fb.get("exp_name"), data_dict['exp_name'])
        self.assertEqual(fb.get("gateway_ip"), data_dict['gateway_ip'])
        self.assertEqual(fb.get("responses")[0].get("question").get("name"),
                             'How is your breakfast?')


    def test_add_feedback_with_saved_answers_in_system_interface(self):
        print "test_add_feedback_with_saved_answers_in_system_interface"

        answer_cls = System.delegate.entities['answer']
        answer = answer_cls(name='yes')
        answer.save()
        version = "open-edx-virtual-labs-v2.0"
        user_id = "John123"
        data_dict = {'lab_name': 'data structure',
                    'exp_name': 'tuples',
                    'key' : KEY,
                    'gateway_ip': '10.4.12.24',
                    'version': version,
                    'user_id': user_id,
                    'responses': [{'name': 'How is your breakfast?',
                                    'answers':['yes', 'no'] }]
                   }

        fb = SystemInterface.add_feedback(data_dict)

        data_dict1 = {'lab_name': "Automata",
            'exp_name': "DFA",
            'key' : KEY,
            'gateway_ip': 'X.X.X.X',
            'version': version,
            'user_id': user_id,
            'responses': [{'name': 'How is your breakfast?',
                            'answers':['yes', 'no'] }]
           }

        fb = SystemInterface.add_feedback(data_dict1)
        
        feedback_cls = System.delegate.entities['feedback']
        response_cls = System.delegate.entities['response']
        fb = feedback_cls.get_by_id(2)
        
        self.assertEqual(2, len(feedback_cls.get_all()))
        self.assertEqual(1, len(response_cls.get_all()))
        self.assertEqual(fb.get("lab_name"), data_dict1['lab_name'])
        self.assertEqual(fb.get("exp_name"), data_dict1['exp_name'])
        self.assertEqual(fb.get("gateway_ip"), data_dict1['gateway_ip'])
        self.assertEqual(fb.get("version"), data_dict1['version'])
        self.assertEqual(fb.get("user_id"), data_dict1['user_id'])
        self.assertEqual(fb.get("responses")[0].get("question").get("name"),
                             'How is your breakfast?')


    def test_add_feedback_raises_type_error_in_system_interface(self):
        print "test_add_feedback_raises_type_error_in_system_interface"
        version = "open-edx-virtual-labs-v2.0"
        user_id = "John123"
        data_dict = {'lab_name': 'data structure',
                    'exp_name': 'tuples',
                    'key' : KEY,
                    'gateway_ip': '10.4.12.24',
                    'version': version,
                    'user_id': user_id,
                    'responses': "hello"
                   }

        with self.assertRaises(TypeError):
            SystemInterface.add_feedback(data_dict)

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

    def test_add_feedback_in_system_interface(self):
        print "test_add_feedback_in_system_interface"

        version = "open-edx-virtual-labs-v2.0"
        user_id = "John123"
        data_dict = {'lab_name': 'data structure',
                    'exp_name': 'tuples',
                    'key' : KEY,
                    'gateway_ip': '10.4.12.24',
                    'version': version,
                    'user_id': user_id,
                    'responses': [{'name': 'How is your breakfast?',
                                    'answers':['yes', 'no'] }]
                   }

        fb = SystemInterface.add_feedback(data_dict)
        feedback_cls = System.delegate.entities['feedback']
        fb = feedback_cls.get_all()[0]
        
        self.assertEqual(fb.get("lab_name"), data_dict['lab_name'])
        self.assertEqual(fb.get("exp_name"), data_dict['exp_name'])
        self.assertEqual(fb.get("gateway_ip"), data_dict['gateway_ip'])
        self.assertEqual(fb.get("responses")[0].get("question").get("name"),
                             'How is your breakfast?')


    def test_add_feedback_with_saved_answers_in_system_interface(self):
        print "test_add_feedback_with_saved_answers_in_system_interface"

        answer_cls = System.delegate.entities['answer']
        answer = answer_cls(name='yes')
        answer.save()
        version = "open-edx-virtual-labs-v2.0"
        user_id = "John123"
        data_dict = {'lab_name': 'data structure',
                    'exp_name': 'tuples',
                    'key' : KEY,
                    'gateway_ip': '10.4.12.24',
                    'version': version,
                    'user_id': user_id,
                    'responses': [{'name': 'How is your breakfast?',
                                    'answers':['yes', 'no'] }]
                   }

        fb = SystemInterface.add_feedback(data_dict)

        data_dict1 = {'lab_name': "Automata",
            'exp_name': "DFA",
            'key' : KEY,
            'gateway_ip': 'X.X.X.X',
            'version': version,
            'user_id': user_id,
            'responses': [{'name': 'How is your breakfast?',
                            'answers':['yes', 'no'] }]
           }

        fb = SystemInterface.add_feedback(data_dict1)
        
        feedback_cls = System.delegate.entities['feedback']
        response_cls = System.delegate.entities['response']
        fb = feedback_cls.get_by_id(2)
        
        
        self.assertEqual(2, len(feedback_cls.get_all()))
        self.assertEqual(1, len(response_cls.get_all()))
        self.assertEqual(fb.get("lab_name"), data_dict1['lab_name'])
        self.assertEqual(fb.get("exp_name"), data_dict1['exp_name'])
        self.assertEqual(fb.get("gateway_ip"), data_dict1['gateway_ip'])
        self.assertEqual(fb.get("version"), data_dict1['version'])
        self.assertEqual(fb.get("user_id"), data_dict1['user_id'])
        self.assertEqual(fb.get("responses")[0].get("question").get("name"),
                             'How is your breakfast?')


    def test_add_feedback_raises_type_error_in_system_interface(self):
        print "test_add_feedback_raises_type_error_in_system_interface"
        version = "open-edx-virtual-labs-v2.0"
        user_id = "John123"
        data_dict = {'lab_name': 'data structure',
                    'exp_name': 'tuples',
                    'key' : KEY,
                    'gateway_ip': '10.4.12.24',
                    'version': version,
                    'user_id': user_id,
                    'responses': "hello"
                   }

        with self.assertRaises(TypeError):
            SystemInterface.add_feedback(data_dict)

class TestAddGenericLabAndExpFeedback(TestCase):
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

    def test_add_generic_lab_feedback_in_system_interface(self):
        print "test_add_generic_lab_feedback_in_system_interface"

        version = "generic-lab-feedback-v2.0"

        data_dict = {'lab_name': 'data structure',
                    'gateway_ip': '10.4.12.24',
                    'key' : KEY,
                    'version': version,
                    'responses': [{'name': 'How is your breakfast?',
                                    'answers':['yes', 'no'] }]
                   }

        fb = SystemInterface.add_feedback(data_dict)
        feedback_cls = System.delegate.entities['feedback']
        fb = feedback_cls.get_all()[0]
        
        self.assertEqual(fb.get("lab_name"), data_dict['lab_name'])
        self.assertEqual(fb.get("gateway_ip"), data_dict['gateway_ip'])
        self.assertEqual(fb.get("responses")[0].get("question").get("name"),
                             'How is your breakfast?')

    def test_add_generic_exp_feedback_in_system_interface(self):
        print "test_add_generic_exp_feedback_in_system_interface"

        version = "generic-exp-feedback-v2.0"

        data_dict = {'lab_name': 'Problem Solving',
                     'exp_name': 'Number Systems',
                    'gateway_ip': '10.4.12.24',
                    'version': version,
                    'key' : KEY,
                    'responses': [{'name': 'How is your breakfast?',
                                    'answers':['yes', 'no'] }]
                   }

        fb = SystemInterface.add_feedback(data_dict)
        feedback_cls = System.delegate.entities['feedback']
        fb = feedback_cls.get_all()[0]
        
        self.assertEqual(fb.get("lab_name"), data_dict['lab_name'])
        self.assertEqual(fb.get("exp_name"), data_dict['exp_name'])
        self.assertEqual(fb.get("gateway_ip"), data_dict['gateway_ip'])
        self.assertEqual(fb.get("responses")[0].get("question").get("name"),
                             'How is your breakfast?')

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

    def test_get_feedback_usage_in_system_interface(self):
        print "test_get_feedback_usage_in_system_interface"

        version = "open-edx-virtual-labs-v2.0"
        user_id = "John123"
        data_dict = {'lab_name': 'data structure',
                    'exp_name': 'tuples',
                    'key' : KEY,
                    'gateway_ip': '10.4.12.24',
                    'version': version,
                    'user_id': user_id,
                    'responses': [{'name': 'How is your breakfast?',
                                    'answers':['yes', 'no'] }]
                   }

        feedback = SystemInterface.add_feedback(data_dict)

        date_obj = datetime.datetime.now().date()
        date = date_obj.strftime('%d-%m-%Y')

        gateway_ip = "10.4.12.24"
        key = KEY
        usage = SystemInterface.get_feedback_usage(gateway_ip, date, key)
        self.assertEqual(usage, 1)

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

    def test_add_feedback_dump_in_system_interface(self):
        print "test_get_feedback_dump_in_system_interface"
        user_id = "John123"
        version = "open-edx-virtual-labs-v2.0"
        data_dict = {'lab_name': 'data structure',
                    'exp_name': 'tuples',
                    'key' : KEY,
                    'gateway_ip': '10.4.12.24',
                    'version': version,
                    'user_id': user_id,
                    'responses': [{'name': 'How is your breakfast?',
                                    'answers':['yes', 'no'] }]
                   }

        feedback = SystemInterface.add_feedback(data_dict)

        date_obj = datetime.datetime.now().date()
        date = date_obj.strftime('%d-%m-%Y')

        key = KEY

        feedbacks = SystemInterface.get_feedback_dump(date, key)
        date_1 = datetime.datetime.strptime(date, "%d-%m-%Y").date()

        self.assertEqual(feedbacks[0]['date'], date_1.strftime('%d-%m-%Y'))

class TestAddQuestion(TestCase):
    TESTING = True
    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_question_in_system_interface(self):
        print "test_add_question_in_system_interface"

        data_dict = {
                    'key' : KEY,
                    'name': 'how are you?',
                    'question_type': 'radio'
                   }

        data_dict1 = {
                    'key' : KEY,
                    'name': 'how are labs?',
                    'question_type': 'radio'
                   }

        question = SystemInterface.add_question(data_dict)
        question1 = SystemInterface.add_question(data_dict1)
        
        self.assertEqual(question.get("question_type"), 
                             data_dict['question_type'])
        self.assertEqual(question.get("name"), data_dict['name'])
        self.assertEqual(question1.get("question_type"), 
                             data_dict1['question_type'])
        self.assertEqual(question1.get("name"), data_dict1['name'])


    def test_add_question_raises_type_error_in_system_interface(self):
        print "test_add_question_raises_type_error_in_system_interface"

        data_dict = {
                    'key' : KEY,
                    'name': 'how are you?',
                    'question_type': 123
                   }

        with self.assertRaises(TypeError):
            SystemInterface.add_question(data_dict)

class TestUpdateQuestion(TestCase):
    TESTING = True
    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_update_question_name_in_system_interface(self):
        print "test_update_question_name_in_system_interface"

        data_dict = {
                    'key' : KEY,
                    'name': 'how are you?',
                    'question_type': 'radio'
                   }

        data_dict1 = {
                    'key' : KEY,
                    'q_id': 1,
                    'name': 'how are labs?'
                   }

        question = SystemInterface.add_question(data_dict)
        question1 = SystemInterface.update_question(data_dict1)
        
        self.assertEqual(question1.get("name"), data_dict1['name'])
        self.assertEqual(question1.get("question_type"),
                             data_dict['question_type'])

    def test_update_question_type_in_system_interface(self):
        print "test_update_question_type_in_system_interface"

        data_dict = {
                    'key' : KEY,
                    'name': 'how are you?',
                    'question_type': 'radio'
                   }

        data_dict1 = {
                    'key' : KEY,
                    'q_id': 1,
                    'question_type': 'text'
                   }

        question = SystemInterface.add_question(data_dict)
        question1 = SystemInterface.update_question(data_dict1)
        
        self.assertEqual(question1.get("name"), data_dict['name'])
        self.assertEqual(question1.get("question_type"), 
                             data_dict1['question_type'])

    def test_update_question_name_and_type_in_system_interface(self):
        print "test_update_question_name_and_type_in_system_interface"

        data_dict = {
                    'key' : KEY,
                    'name': 'how are you?',
                    'question_type': 'radio'
                   }

        data_dict1 = {
                    'key' : KEY,
                    'q_id': 1,
                    'name': 'how are labs?',
                    'question_type': 'text'
                   }

        question = SystemInterface.add_question(data_dict)
        question1 = SystemInterface.update_question(data_dict1)
        
        self.assertEqual(question1.get("name"), data_dict1['name'])
        self.assertEqual(question1.get("question_type"), 
                                        data_dict1['question_type'])

class TestDeleteQuestion(TestCase):
    TESTING = True
    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_delete_question_in_system_interface(self):
        print "test_delete_question_in_system_interface"

        data_dict = {
                    'key' : KEY,
                    'name': 'how are labs?',
                    'question_type': 'radio'
                   }

        data_dict1 = {
                    'key' : KEY,
                    'name': 'how are experiments?',
                    'question_type': 'text'
                   }

        question = SystemInterface.add_question(data_dict)
        question1 = SystemInterface.add_question(data_dict1)
        q_id = SystemInterface.delete_question(1)
        
        self.assertEqual(q_id, 1)

class TestGetQuestions(TestCase):
    TESTING = True
    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_questions_in_system_interface(self):
        print "test_get_questions_in_system_interface"

        data_dict = {
                    'key' : KEY,
                    'name': 'how are you?',
                    'question_type': 'radio'
                   }

        data_dict1 = {
                    'key' : KEY,
                    'name': 'how are labs?',
                    'question_type': 'text'
                   }

        question1 = SystemInterface.add_question(data_dict)
        question2 = SystemInterface.add_question(data_dict1)

        questions_list = SystemInterface.get_questions()
        
        self.assertEqual(questions_list[0].get("name"), data_dict['name'])
        self.assertEqual(questions_list[1].get("name"), data_dict1['name'])
        self.assertEqual(questions_list[0].get("question_type"), 
                             data_dict['question_type'])
        self.assertEqual(questions_list[1].get("question_type"), 
                             data_dict1['question_type'])

class TestGetQuestionById(TestCase):
    TESTING = True
    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_question_by_id_in_system_interface(self):
        print "test_get_question_by_id_in_system_interface"

        data_dict = {
                    'key' : KEY,
                    'name': 'how are you?',
                    'question_type': 'radio'
                   }

        data_dict1 = {
                    'key' : KEY,
                    'name': 'how are labs?',
                    'question_type': 'text'
                   }

        question1 = SystemInterface.add_question(data_dict)
        question2 = SystemInterface.add_question(data_dict1)

        question_data_one = SystemInterface.get_question_by_id(1)
        question_data_two = SystemInterface.get_question_by_id(2)
        
        self.assertEqual(question_data_one.get("name"), data_dict['name'])
        self.assertEqual(question_data_two.get("name"), data_dict1['name'])
        self.assertEqual(question_data_one.get("question_type"), 
                             data_dict['question_type'])
        self.assertEqual(question_data_two.get("question_type"), 
                             data_dict1['question_type'])

if __name__ == '__main__':
    unittest.main()
