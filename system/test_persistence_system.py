
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import unittest
from flask_testing import TestCase
from runtime.rest.app import create_app
from runtime.system.system import *
from runtime.config.system_config import KEY
from runtime.utils.class_persistence_template import db

config = {
         'SQLALCHEMY_DATABASE_URI': ''
         }

def populate_db():
    pass
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

    def test_add_question(self):
        
        print "test_add_question_in_system_persistence"
        session_cls = System.delegate.entities['session']
        response_cls = System.delegate.entities['response']
        question_cls = System.delegate.entities['question']
        answer_cls = System.delegate.entities['answer']
        feedback_cls = System.delegate.entities['feedback']

        name="how are labs?"
        radio="radio"
        key = KEY
        session = session_cls(key=key)
        question = question_cls(name=name, question_type=radio)
        question1 = System.do("add_question", question=question,
                                  session=session)
        new_question = question_cls.get_by_id(1)
        self.assertEqual(new_question.get("name"), name)
            
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

    def test_delete_question(self):
        
        print "test_delete_question_in_system_persistence"
        session_cls = System.delegate.entities['session']
        question_cls = System.delegate.entities['question']

        name="how are labs?"
        radio="radio"
        key = KEY
        session = session_cls(key=key)
        question = question_cls(name=name, question_type=radio)
        question1 = System.do("add_question", question=question,
                                  session=session)

        name1="how are experiments?"
        radio1="text"
        question1 = question_cls(name=name1, question_type=radio1)
        question2 = System.do("add_question", question=question1,
                                  session=session)

        System.do("delete_question", q_id=1, session=session)

        self.assertEqual(len(question_cls.get_all()), 1)
            
class TestAddAnswer(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_answer(self):
        print "test_add_answer_in_system_persistence"
        session_cls = System.delegate.entities['session']
        response_cls = System.delegate.entities['response']
        question_cls = System.delegate.entities['question']
        answer_cls = System.delegate.entities['answer']
        feedback_cls = System.delegate.entities['feedback']

        ans = "excellent labs"
        answer = answer_cls(name=ans)
        key = KEY
        session = session_cls(key=key)
        answer = System.do("add_answer", answer=answer, session=session)
        answer1 = answer_cls.get_by_id(1)
        self.assertEqual(answer1.get("name"), ans)
            
class TestAddFeedback(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_feedback(self):
        print "test_add_feedback_in_system_persistence"
        session_cls = System.delegate.entities['session']
        response_cls = System.delegate.entities['response']
        question_cls = System.delegate.entities['question']
        answer_cls = System.delegate.entities['answer']
        feedback_cls = System.delegate.entities['feedback']
        version = "open-edx-virtual-labs-v2.0"
        user_id = "John123"
        date = datetime.datetime.now().date()

        data_dict = {'lab_name': 'data structure',
                    'exp_name': 'tuples',
                    'key' : KEY,
                    'gateway_ip': '10.4.12.24',
                    'date': date,
                    'version': version,
                    'user_id': user_id,
                    'responses': [] 
                   }
        data_dict['session'] = session_cls(key=data_dict['key'])
        del(data_dict['key'])
        feedback = System.do("add_feedback", **data_dict)

        fb = feedback_cls.get_by_id(1)
        self.assertEqual(fb.get("gateway_ip"), '10.4.12.24')
        self.assertEqual(fb.get("lab_name"), 'data structure')
        self.assertEqual(fb.get("exp_name"), 'tuples')
        self.assertEqual(fb.get("version"), version)
        self.assertEqual(fb.get("user_id"), user_id)
        self.assertEqual(fb.get("responses"), [])
            
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

    def test_update_question(self):
        
        print "test_update_question_in_system_persistence"
        session_cls = System.delegate.entities['session']
        question_cls = System.delegate.entities['question']

        name="how are labs?"
        radio="radio"
        key = KEY
        session = session_cls(key=key)
        question = question_cls(name=name, question_type=radio)
        question1 = System.do("add_question", question=question,
                                  session=session)
        name1="how are experiements?"
        radio1="text"
        question1 = System.do("update_question", question=question,
                                  name=name1, question_type=radio1,
                                  session=session)

        new_question = question_cls.get_by_id(1)

        self.assertEqual(new_question.get("name"), name1)
        self.assertEqual(new_question.get("question_type"), radio1)
            
class TestGetFeedbackUsage(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_feedback_usage(self):
        print "test_get_feedback_usage_in_system_persistence"
        session_cls = System.delegate.entities['session']
        response_cls = System.delegate.entities['response']
        question_cls = System.delegate.entities['question']
        answer_cls = System.delegate.entities['answer']
        feedback_cls = System.delegate.entities['feedback']
        
        user_id = "John123"
        version = "open-edx-virtual-labs-v2.0"
        date = datetime.datetime.now().date()
        data_dict = {'lab_name': 'data structure',
                    'exp_name': 'tuples',
                    'key' : KEY,
                    'gateway_ip': '10.4.12.24',
                    'date': date,
                    'version': version,
                    'user_id': user_id,
                    'responses': [] 
                   }
        data_dict['session'] = session_cls(key=data_dict['key'])
        del(data_dict['key'])
        gateway_ip = "10.4.12.24"
        date = datetime.datetime.now().date()

        feedback = System.do("add_feedback", **data_dict)

        feedback_usage = System.do("get_feedback_usage",
                                       gateway_ip=gateway_ip, 
                                       date=date, 
                                       session=data_dict['session'])
        
        self.assertEqual(feedback_usage, 1)
            
class TestGetFeedbackDump(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_feedback_dump(self):
        print "test_get_feedback_dump_in_system_persistence"
        session_cls = System.delegate.entities['session']
        response_cls = System.delegate.entities['response']
        question_cls = System.delegate.entities['question']
        answer_cls = System.delegate.entities['answer']
        feedback_cls = System.delegate.entities['feedback']

        date = datetime.datetime.now().date()
        version = "open-edx-virtual-labs-v2.0"
        user_id = "John123"
        data_dict = {'lab_name': 'data structure',
                    'exp_name': 'tuples',
                    'key' : KEY,
                    'gateway_ip': '10.4.12.24',
                    'date': date,
                    'version': version,
                    'user_id': user_id,
                    'responses': [] 
                   }
        data_dict['session'] = session_cls(key=data_dict['key'])
        del(data_dict['key'])

        feedback = System.do("add_feedback", **data_dict)

        feedbacks = System.do("get_feedback_dump", date=date, session=data_dict['session'])
        self.assertEqual(feedbacks[0].date, date)
            
class TestAddResponsesToFeedback(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_responses_to_feedback(self):
        print "test_add_responses_to_feedback_in_system_persistence"
        session_cls = System.delegate.entities['session']
        response_cls = System.delegate.entities['response']
        question_cls = System.delegate.entities['question']
        answer_cls = System.delegate.entities['answer']
        feedback_cls = System.delegate.entities['feedback']

        name = "how are labs?"
        q_type = "radio"

        question1 = question_cls(name=name, question_type=q_type)
        question1.save()

        ans = "excellent labs"
        answer1 = answer_cls(name=ans)
        answer1.save()

        gateway_ip = "10.100.40.2"
        lab_name = "cse01"
        exp_name = "data01"
        version = "open-edx-virtual-labs-v2.0"
        user_id = "John123"
        date = datetime.datetime.strptime("30-06-2016", "%d-%m-%Y").date()

        fb = feedback_cls(gateway_ip=gateway_ip,
                      lab_name=lab_name,
                      exp_name=exp_name,
                      date=date,
                      version=version,
                      user_id=user_id,
                      responses=[])
        fb.save()

        res = response_cls(question=question1, answers=[answer1], 
                           feedbacks=[fb])
        key = KEY
        session = session_cls(key=key)
        fb1 = System.do("add_responses_to_feedback", responses=[res],
                                  fb_id=1,
                                  session=session)

        feedback = feedback_cls.get_by_id(1)

        self.assertEqual(feedback.get("lab_name"), lab_name)
        self.assertEqual(feedback.get("responses")[0].get("question").\
                             get("name"), question1.get("name"))
        self.assertEqual(feedback.get("responses")[0].get("answers")[0].\
                             get("name"), answer1.get("name"))

if __name__ == '__main__':
    unittest.main()
