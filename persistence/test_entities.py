
# -*- coding: utf-8 -*-
import unittest
from flask_testing import TestCase
from sqlalchemy.exc import IntegrityError
from runtime.persistence.entities import *
from runtime.rest.app import create_app

config = {
    'SQLALCHEMY_DATABASE_URI': ''
}

class TestPersistentQuestion(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_question(self):
        print "test_create_question"
        name="how are labs?"
        radio="radio"
        question1 = Question(name=name, question_type=radio)
        question1.save()

        new_question = Question.get_by_id(1)
        self.assertEqual(new_question.get("name"), name)
        self.assertEqual(new_question.get("question_type"), radio)

class TestPersistenceAnswer(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_answer(self):
        print "test_create_answer"
        ans = "excellent labs"
        answer = Answer(name=ans)
        answer.save()
        answer = Answer.get_by_id(1)
        self.assertEqual(answer.get("name"), ans)

class TestPersistenceFeedback(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_feedback(self):
        print "test_create_feedback"

        gateway_ip = "10.100.40.2"
        lab_name = "cse01"
        exp_name = "data01"
        date = datetime.datetime.strptime("30-06-2016", "%d-%m-%Y").date()
        version = "open-edx-virtual-labs-v2.0"
        user_id = "John123"
        fb = Feedback(gateway_ip=gateway_ip,
                      lab_name=lab_name,
                      exp_name=exp_name,
                      date=date,
                      version=version,
                      user_id=user_id,
                      responses=[])
        fb.save()

        self.assertEqual(fb.get("gateway_ip"), gateway_ip)
        self.assertEqual(fb.get("lab_name"), lab_name)
        self.assertEqual(fb.get("exp_name"), exp_name)
        self.assertEqual(fb.get("version"), version)
        self.assertEqual(fb.get("user_id"), user_id)
        self.assertEqual(fb.get("responses"), [])

class TestPersistenceResponse(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_response(self):
        print "test_create_response"

        name = "how are labs?"
        q_type = "radio"
        question1 = Question(name=name, question_type=q_type)
        question1.save()

        ans = "excellent labs"
        answer1 = Answer(name=ans)
        answer1.save()

        gateway_ip = "10.100.40.2"
        lab_name = "cse01"
        exp_name = "data01"
        version = "open-edx-virtual-labs-v2.0"
        user_id = "John123"
        date = datetime.datetime.strptime("30-06-2016", "%d-%m-%Y").date()

        fb = Feedback(gateway_ip=gateway_ip,
                      lab_name=lab_name,
                      exp_name=exp_name,
                      date=date,
                      version=version,
                      user_id=user_id,
                      responses=[])
        fb.save()

        res = Response(question=question1, answers=[answer1], feedbacks=[fb])
        res.save()

        response = Response.get_by_id(1)

        self.assertEqual(response.get("question").get("name"), 
                             question1.get("name"))

        self.assertEqual(response.get("answers")[0].get("name"), 
                             answer1.get("name"))

        self.assertEqual(response.get("feedbacks")[0].get("lab_name"), 
                             fb.get("lab_name"))

if __name__ == '__main__':
    unittest.main()
