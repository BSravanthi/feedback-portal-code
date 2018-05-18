
# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase
from entities import *

class TestQuestion(TestCase):
    TESTING = True
    def test_object_question(self):
        print "test_object_question"
        name="how are labs?"
        q_type="radio"
        question = Question(name=name, question_type=q_type)
        self.assertEqual(question.get("name"), name)
        self.assertEqual(question.get("question_type"), q_type)

class TestAnswer(TestCase):
    TESTING = True

    def test_object_answer(self):
        print "test_object_answer"
        ans = "excellent labs"
        answer = Answer(name=ans)
        self.assertEqual(answer.get("name"), ans)

class TestFeedback(TestCase):
    TESTING = True

    def test_object_feedback(self):
        print "test_object_feedback"
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

        self.assertEqual(fb.get("gateway_ip"), gateway_ip)
        self.assertEqual(fb.get("lab_name"), lab_name)
        self.assertEqual(fb.get("exp_name"), exp_name)
        self.assertEqual(fb.get("date"), date)
        self.assertEqual(fb.get("version"), version)
        self.assertEqual(fb.get("user_id"), user_id)
        self.assertEqual(fb.get("responses"), [])

class TestResponse(TestCase):
    TESTING = True

    def test_object_response(self):
        print "test_object_response"

        name = "how are labs?"
        q_type = "radio"
        question1 = Question(name=name, question_type=q_type)

        ans = "excellent labs"
        answer1 = Answer(name=ans)

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

        res = Response(question=question1, answers=[answer1], feedbacks=[fb])
        fb.set(responses=[res])

        self.assertEqual(res.get("question").get("name"), 
                             question1.get("name"))

        self.assertEqual(res.get("answers")[0].get("name"), 
                             answer1.get("name"))

        self.assertEqual(res.get("feedbacks")[0].get("gateway_ip"), 
                             gateway_ip)


if __name__ == '__main__':
    unittest.main()
