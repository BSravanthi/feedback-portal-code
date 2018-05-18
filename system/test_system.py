
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import unittest
from flask_testing import TestCase
from runtime.rest.app import create_app
from runtime.system.system import *
from runtime.system.persistence_delegate import *

config = {
         'SQLALCHEMY_DATABASE_URI': ''
         }

class TestSystemConstructor(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        System.initialize_system(PersistenceDelegate)

    def tearDown(self):
        System.delegate = None

    def test_delegate(self):
        print "test_delegate"
        self.assertEqual(isinstance(System.delegate, PersistenceDelegate), 
                             True)

    def test_is_session_valid(self):
        print "test_is_session_valid"
        session = Session(key=KEY)
        self.assertEqual(System.is_session_valid(session), True)

    def test_is_session_not_valid(self):
        print "test_is_session_not_valid"
        session = Session(key="jdhfkjhdakjf")
        self.assertEqual(System.is_session_valid(session), False)

    def test_arity(self):
        print "test_arity"
        with self.assertRaises(ArityError):
            System.arity_check([1,2], 3)

    def test_type_checks(self):
        print "test_type_checks"
        args = {"question": Question(name="why", question_type="radio"),
                "answer": Question(name="where", question_type="radio")
                }

        arg_types = {"question": is_question,
                     "answer": is_answer
                     }

        with self.assertRaises(TypeError):
            System.type_check(args, arg_types)

    def test_get_feedback_form(self):
        print "test_get_feedback_form"
        session = Session(key=KEY)
        lab_name = "Data Structures"
        exp_name = "Binary Search"
        user_id = "xyz123"
        version = None
        questions_dict = System.do("get_feedback_form", 
                                      session=session,
                                      lab_name=lab_name,
                                      exp_name=exp_name,
                                      version=None,
                                      user_id=user_id)
                                      
        self.assertEqual(questions_dict['user_id'], user_id)  

if __name__ == '__main__':
    unittest.main()
