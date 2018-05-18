
# -*- coding: utf-8 -*-
import unittest
from flask_testing import TestCase
from runtime.rest.app import create_app
from runtime.system.persistence_delegate import *


config = {
         'SQLALCHEMY_DATABASE_URI': ''
         }
class TestPersistenceDelegate(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()
        self.persistence_delegate = PersistenceDelegate()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.persistence_delegate = None



    def test_get_answer(self):
         print "test_get_answer"

         ans1 = "excellent labs"
         answer1 = Answer(name=ans1)
         answer1.save()

         answer_obj = self.persistence_delegate.get_answer(name=
                                                answer1.get("name"))
         self.assertEqual(answer_obj.get("name"),
                              answer1.get("name"))

    def test_get_responses(self):
         print "test_get_responses"

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
         date = datetime.datetime.strptime("30-06-2016", "%d-%m-%Y").date()
         user_id = "John123"

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
         
         question = res.get("question")
         answers = res.get("answers")

         responses = self.persistence_delegate.get_responses(\
                                                      question=question)
         self.assertEqual(responses[0].get("question").get("name"),
                              res.get("question").get("name"))
         self.assertEqual(responses[0].get("answers")[0].get("name"),
                              res.get("answers")[0].get("name"))

         responses = self.persistence_delegate.get_responses(\
                                                      question=question, 
                                                      answers=['t', 'k'])
         self.assertEqual(responses, [])

    def test_get_response(self):
         print "test_get_response"

         name = "how are labs?"
         q_type = "radio"
         question1 = Question(name=name, question_type=q_type)
         question1.save()

         ans1 = Answer(name="excellent")
         ans1.save()
         ans2 = Answer(name="good")
         ans2.save()

         gateway_ip = "10.100.40.2"
         lab_name = "cse01"
         exp_name = "data01"
         version = "open-edx-virtual-labs-v2.0"
         date = datetime.datetime.strptime("30-06-2016", "%d-%m-%Y").date()
         user_id = "John123"
         fb = Feedback(gateway_ip=gateway_ip,
                        lab_name=lab_name,
                        exp_name=exp_name,
                        date=date,
                        version=version,
                        user_id = user_id,
                        responses=[])
         fb.save()

         res1 = Response(question=question1, answers=[ans1], feedbacks=[fb])
         res1.save()
         res2 = Response(question=question1, answers=[ans1, ans2], 
                             feedbacks=[fb])
         res2.save()
     
         res3 = Response(question=question1, answers=[ans2], feedbacks=[fb])
         res3.save()
         
         response_obj = self.persistence_delegate.get_response(\
                question=question1, answers=[ans1, ans2])
         self.assertEqual(response_obj.get("question").get("name"),
                              question1.get("name"))
         self.assertEqual(response_obj.get("answers")[0].get("name"),
                              ans1.get("name"))
         self.assertEqual(response_obj.get("answers")[1].get("name"),
                              ans2.get("name"))

         response_obj = self.persistence_delegate.get_response(\
                question=question1, answers=[ans1])
         self.assertEqual(response_obj.get("question").get("name"),
                              question1.get("name"))
         self.assertEqual(response_obj.get("answers")[0].get("name"),
                              ans1.get("name"))
                              

    def test_question_exists(self):
        print "test_question_exists"
        name1="how are labs?"
        radio="radio"
        question1 = Question(name=name1, question_type=radio)
        question = self.persistence_delegate.add_question(question1)

        name2="how are experiments?"
        question2 = Question(name=name2, question_type=radio)
        
        self.assertEqual(self.persistence_delegate.question_exists(question),
                            True)
        self.assertEqual(self.persistence_delegate.question_exists(question2),
                            False)

    def test_answer_exists(self):
        print "test_answer_exists"

        ans1 = "excellent labs"
        answer1 = Answer(name=ans1)
        self.persistence_delegate.add_answer(answer1)

        ans2 = "excellent"
        answer2 = Answer(name=ans2)
        
        self.assertEqual(self.persistence_delegate.answer_exists(answer1),
                            True)
        self.assertEqual(self.persistence_delegate.answer_exists(answer2),
                            False)

    def test_feedback_exists(self):
        print "test_feedback_exists"
        gateway_ip1 = "10.100.40.2"
        lab_name1 = "cse01"
        exp_name1 = "data01"
        date1 = datetime.datetime.strptime("30-06-2016", "%d-%m-%Y").date()
        version = "open-edx-virtual-labs-v2.0"
        user_id = "John123"
        fb1 = Feedback(gateway_ip=gateway_ip1,
                        lab_name=lab_name1,
                        exp_name=exp_name1,
                        date=date1,
                        version=version,
                        user_id=user_id,
                        responses=[])
        fb1.save()

        gateway_ip2 = "10.100.50.2"
        lab_name2 = "cse02"
        exp_name2 = "data02"
        date2 = datetime.datetime.strptime("30-06-2017", "%d-%m-%Y").date()
        version2 = "open-edx-virtual-labs-v1.0"
        user_id = "John123"
        fb2 = Feedback(gateway_ip=gateway_ip2,
                                lab_name=lab_name2,
                                exp_name=exp_name2,
                                date=date2,
                                version=version2,
                                user_id=user_id,
                                responses=[]
                                )
        
        self.assertEqual(self.persistence_delegate.feedback_exists(1),
                            True)
        self.assertEqual(self.persistence_delegate.feedback_exists(2),
                            False)

    def test_response_exists(self):
        print "test_response_exists"

        name = "how are labs?"
        q_type = "radio"
        question1 = Question(name=name, question_type=q_type)
        question1.save()

        ans1 = Answer(name="excellent")
        ans1.save()
        ans2 = Answer(name="good")
        ans2.save()
        
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

        res1 = Response(question=question1, answers=[ans1], feedbacks=[fb])
        res1.save()
        res2 = Response(question=question1, answers=[ans1, ans2], 
                            feedbacks=[fb])
        res2.save()

        res3 = Response(question=question1, answers=[ans2], feedbacks=[fb])

        ret_val_dict = self.persistence_delegate.response_exists(res1)
        self.assertEqual(ret_val_dict['exists'], True)

        ret_val_dict = self.persistence_delegate.response_exists(res2)
        self.assertEqual(ret_val_dict['exists'], True)

        ret_val_dict = self.persistence_delegate.response_exists(res3)
        self.assertEqual(ret_val_dict['exists'], False)

    def test_add_question(self):
         print "test_add_question"
         name = "how are labs?"
         question_type = "radio"
         question = Question(name=name, question_type=question_type)
         question1 = self.persistence_delegate.add_question(question)
         self.assertEqual(self.persistence_delegate.question_exists(question1),
                          True)

    def test_delete_question(self):
         print "test_delete_question"
         name = "how are labs?"
         question_type = "radio"
         question = Question(name=name, question_type=question_type)
         question1 = self.persistence_delegate.add_question(question)

         name1 = "how are experiments?"
         question_type1 = "radio"
         question1 = Question(name=name1, question_type=question_type1)
         question2 = self.persistence_delegate.add_question(question1)

         self.persistence_delegate.delete_question(1)

         self.assertEqual(len(Question.get_all()), 1)

    def test_add_answer(self):
         print "test_add_answer"
         ans = "excellent labs"
         answer = Answer(name=ans)
         answer1 = self.persistence_delegate.add_answer(answer)
         answer1 = Answer.get_by_id(1)
         self.assertEqual(answer1.get("name"), ans)

    def test_add_feedback(self):
         print "test_add_feedback"
         gateway_ip = "10.100.40.2"
         lab_name = "cse01"
         exp_name = "data01"
         date = datetime.datetime.strptime("30-06-2016", "%d-%m-%Y").date()
         version = "open-edx-virtual-labs-v2.0"
         user_id = "John123"
         responses = []

         try:
            fb1 = self.persistence_delegate.add_feedback(gateway_ip, lab_name,
                                                         exp_name, date, 
                                                         version,
                                                         user_id,
                                                         responses)
         except Exception as err:
             self.assertEqual(True, False)

         feedback = Feedback.get_by_id(1)

         self.assertEqual(feedback.get("gateway_ip"), gateway_ip)
         self.assertEqual(feedback.get("lab_name"), lab_name)
         self.assertEqual(feedback.get("exp_name"), exp_name)
         self.assertEqual(feedback.get("responses"), [])
         self.assertEqual(feedback.get("date"), date)
         self.assertEqual(feedback.get("version"), version)
         self.assertEqual(feedback.get("user_id"), user_id)

    def test_update_question(self):
         print "test_update_question"
         name = "how are labs?"
         question_type = "radio"
         question = Question(name=name, question_type=question_type)
         question1 = self.persistence_delegate.add_question(question)
         name1 = "how are experiments?"
         question_type1 = "text"
         question2 = self.persistence_delegate.update_question\
           (question1, name1, question_type1),
         question2 = Question.get_by_id(1)
         self.assertEqual(question2.get("name"), name1)

    def test_get_feedbacks(self):
         print "test_persistence_get_feedbacks"

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
         date = datetime.datetime.strptime("30-06-2016", "%d-%m-%Y").date()
         user_id = "John123"

         fb = Feedback(gateway_ip=gateway_ip,
                        lab_name=lab_name,
                        exp_name=exp_name,
                        date=date,
                        version=version,
                        user_id=user_id,
                        responses=[])
         fb.save()

         feedback_obj = self.persistence_delegate.get_feedbacks(gateway_ip=\
                                                        gateway_ip, date=date)
         self.assertEqual(feedback_obj[0].get("gateway_ip"),
                              gateway_ip)
         self.assertEqual(feedback_obj[0].get("date"), date)

    def test_get_feedback_by_id(self):
         print "test_persistence_get_feedback_by_id"

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
         date = datetime.datetime.strptime("30-06-2016", "%d-%m-%Y").date()
         user_id = "John123"
         fb = Feedback(gateway_ip=gateway_ip,
                        lab_name=lab_name,
                        exp_name=exp_name,
                        date=date,
                        version=version,
                        user_id = user_id,
                        responses=[])
         fb.save()

         feedback_obj = self.persistence_delegate.get_feedback_by_id(1)
         self.assertEqual(feedback_obj.get("gateway_ip"),
                              gateway_ip)
         self.assertEqual(feedback_obj.get("date"), date)

    def test_get_feedback_usage(self):
         print "test_get_feedback_usage"
         gateway_ip1 = "10.100.40.2"
         lab_name1 = "cse01"
         exp_name1 = "data01"
         version = "open-edx-virtual-labs-v2.0"
         date1 = datetime.datetime.strptime("30-06-2016", "%d-%m-%Y").date()
         responses1 = []
         user_id = "John123"
         fb1 = self.persistence_delegate.add_feedback(gateway_ip1, lab_name1,
                                                        exp_name1, date1,
                                                        version,
                                                        user_id,
                                                        responses1)
         gateway_ip2 = "10.100.40.2"
         lab_name2 = "cse02"
         exp_name2 = "data02"
         version2 = "open-edx-virtual-labs-v1.0"
         date2 = datetime.datetime.strptime("30-06-2016", "%d-%m-%Y").date()
         responses2 = []
         fb2 = self.persistence_delegate.add_feedback(gateway_ip2, lab_name2,
                                                        exp_name2, date2,
                                                        version2,
                                                        user_id,
                                                        responses2)
         usage = self.persistence_delegate.get_feedback_usage(gateway_ip2, 
                                                                 date2)

         self.assertEqual(usage, 2)

    def test_get_feedback_dump(self):
         print "test_get_feedback_dump"
         gateway_ip1 = "10.100.40.2"
         lab_name1 = "cse01"
         exp_name1 = "data01"
         version1 = "open-edx-virtual-labs-v1.0"
         date1 = datetime.datetime.strptime("30-06-2016", "%d-%m-%Y").date()
         responses1 = []
         user_id = "John123"
         fb1 = self.persistence_delegate.add_feedback(gateway_ip1, lab_name1,
                                                        exp_name1, date1,
                                                        version1,
                                                        user_id,
                                                        responses1)
         gateway_ip2 = "10.100.40.2"
         lab_name2 = "cse02"
         exp_name2 = "data02"
         date2 = datetime.datetime.strptime("30-06-2016", "%d-%m-%Y").date()
         responses2 = []
         version2 = "open-edx-virtual-labs-v2.0"
         fb2 = self.persistence_delegate.add_feedback(gateway_ip2, lab_name2,
                                                        exp_name2, date2,
                                                        version2,
                                                        user_id,
                                                        responses2)
         feedbacks = self.persistence_delegate.get_feedback_dump(date2)

         self.assertEqual(feedbacks[0].date, date1)
         self.assertEqual(feedbacks[0].gateway_ip, gateway_ip1)

    def test_add_saved_responses_to_feedback(self):
         print "test_add_saved_responses_to_feedback"

         q_type = "radio"
         question1 = Question(name="How is your breakfast?", 
                                  question_type=q_type)
         question2 = Question(name="How is your lunch?", question_type=q_type)
         question3 = Question(name="How is your dinner?", question_type=q_type)

         q1 = Question(name="How is your breakfast?", 
                                  question_type=q_type)
         q2 = Question(name="How is your lunch?", question_type=q_type)
         q3 = Question(name="How is your dinner?", question_type=q_type)


         answer1 = Answer(name="Good")
         answer2 = Answer(name="Bad")
         answer3 = Answer(name="Excellent")
         answer4 = Answer(name="Fair")

         a1 = Answer(name="Good")
         a2 = Answer(name="Bad")
         a3 = Answer(name="Excellent")
         a4 = Answer(name="Fair")

         question1.save()
         question2.save()
         question3.save()

         answer1.save()
         answer2.save()
         answer3.save()
         answer4.save()

         gateway_ip = "10.100.40.2"
         lab_name = "cse01"
         exp_name = "data01"
         version = "open-edx-virtual-labs-v2.0"
         date = datetime.datetime.strptime("30-06-2016", "%d-%m-%Y").date()
         user_id = "John123"
         fb = Feedback(gateway_ip=gateway_ip,
                        lab_name=lab_name,
                        exp_name=exp_name,
                        date=date,
                        version=version,
                        user_id=user_id,
                        responses=[])
         fb.save()

         res1 = Response(question=question1, answers=[answer1], feedbacks=[fb])
         res2 = Response(question=question2, answers=[answer2, answer3], 
                             feedbacks=[fb])
         res3 = Response(question=question3, answers=[answer3], feedbacks=[fb])
         res4 = Response(question=question3, 
                             answers=[answer1, answer2, answer3, answer4], 
                             feedbacks=[fb])


         r1 = Response(question=q1, answers=[a1], feedbacks=[fb])
         r2 = Response(question=q2, answers=[a2, answer3], 
                             feedbacks=[fb])
         r3 = Response(question=q3, answers=[a3], feedbacks=[fb])
         r4 = Response(question=q3, 
                             answers=[a1, a2, a3, a4], 
                             feedbacks=[fb])

         res1.save()
         res2.save()
         res3.save()
         res4.save()

         version = "open-edx-virtual-labs-v2.0"
         user_id = "John123"

         fb1 = Feedback(gateway_ip=gateway_ip,
                          lab_name="Finite Automate",
                          exp_name="DFA",
                          date=date,
                          version=version,
                          user_id=user_id,
                          responses=[])
         fb1.save()

         feedback = self.persistence_delegate.add_responses_to_feedback(fb1.id, 
                                                  [r1, r2, r3, r4])

         self.assertEqual(len(feedback.get("responses")), 4)
         self.assertEqual(feedback.get("responses")[0], res1)
         self.assertEqual(feedback.get("responses")[1], res2)
         self.assertEqual(feedback.get("responses")[2], res3)
         self.assertEqual(feedback.get("responses")[3], res4)


    def test_add_unsaved_responses_with_saved_answers_to_feedback(self):
         print "test_add_unsaved_responses_with_saved_answers_to_feedback"

         q_type = "radio"
         question1 = Question(name="How is your breakfast?", 
                                  question_type=q_type)
         question2 = Question(name="How is your lunch?", question_type=q_type)
         question3 = Question(name="How is your dinner?", question_type=q_type)


         answer1 = Answer(name="Good")
         answer2 = Answer(name="Bad")
         answer3 = Answer(name="Excellent")
         answer4 = Answer(name="Fair")

         question1.save()
         question2.save()
         question3.save()

         answer1.save()
         answer2.save()
         answer3.save()
         answer4.save()

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

         res1 = Response(question=question1, answers=[answer1], feedbacks=[fb])
         res2 = Response(question=question2, answers=[answer2, answer3], 
                             feedbacks=[fb])
         res3 = Response(question=question3, answers=[answer3], feedbacks=[fb])
         res4 = Response(question=question3, 
                             answers=[answer1, answer2, answer3, answer4], 
                             feedbacks=[fb])


         feedback = self.persistence_delegate.add_responses_to_feedback(1, 
                                                  [res1, res2, res3, res4])

         self.assertEqual(len(feedback.get("responses")), 4)
         self.assertEqual(feedback.get("responses")[0], res1)
         self.assertEqual(feedback.get("responses")[1], res2)
         self.assertEqual(feedback.get("responses")[2], res3)
         self.assertEqual(feedback.get("responses")[3], res4)


    def test_add_unsaved_responses_with_unsaved_answers_to_feedback(self):
         print "test_add_unsaved_responses_with_saved_answers_to_feedback"

         q_type = "radio"
         question1 = Question(name="How is your breakfast?", 
                                  question_type=q_type)
         question2 = Question(name="How is your lunch?", question_type=q_type)
         question3 = Question(name="How is your dinner?", question_type=q_type)


         answer1 = Answer(name="Good")
         answer2 = Answer(name="Bad")
         answer3 = Answer(name="Excellent")
         answer4 = Answer(name="Fair")

         question1.save()
         question2.save()
         question3.save()

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

         res1 = Response(question=question1, answers=[answer1], feedbacks=[fb])
         res2 = Response(question=question2, answers=[answer2, answer3], 
                             feedbacks=[fb])
         res3 = Response(question=question3, answers=[answer3], feedbacks=[fb])
         res4 = Response(question=question3, 
                             answers=[answer1, answer2, answer3, answer4], 
                             feedbacks=[fb])


         feedback = self.persistence_delegate.add_responses_to_feedback(1, 
                                                  [res1, res2, res3, res4])

         self.assertEqual(len(feedback.get("responses")), 4)
         self.assertEqual(feedback.get("responses")[0], res1)
         self.assertEqual(feedback.get("responses")[1], res2)
         self.assertEqual(feedback.get("responses")[2], res3)
         self.assertEqual(feedback.get("responses")[3], res4)

    def test_add_p_saved_responses_with_p_saved_answers_to_feedback(self):
         print "test_add_p_saved_responses_with_p_saved_answers_to_feedback"
         print "p refers to partially saved"

         q_type = "radio"
         question1 = Question(name="How is your breakfast?", 
                                  question_type=q_type)
         question2 = Question(name="How is your lunch?", question_type=q_type)
         question3 = Question(name="How is your dinner?", question_type=q_type)


         answer1 = Answer(name="Good")
         answer2 = Answer(name="Bad")
         answer3 = Answer(name="Excellent")
         answer4 = Answer(name="Fair")

         answer1.save()
         answer2.save()

         question1.save()
         question2.save()
         question3.save()

         gateway_ip = "10.100.40.2"
         lab_name = "cse01"
         exp_name = "data01"
         version = "open-edx-virtual-labs-v2.0"
         date = datetime.datetime.strptime("30-06-2016", "%d-%m-%Y").date()
         user_id = "John123"
         fb = Feedback(gateway_ip=gateway_ip,
                        lab_name=lab_name,
                        exp_name=exp_name,
                        date=date,
                        version=version,
                        user_id=user_id,
                        responses=[])
         fb.save()

         res1 = Response(question=question1, answers=[answer1], feedbacks=[fb])
         res2 = Response(question=question2, answers=[answer2, answer1], 
                             feedbacks=[fb])
         res3 = Response(question=question3, answers=[answer3], feedbacks=[fb])
         res4 = Response(question=question3, 
                             answers=[answer1, answer2, answer3, answer4], 
                             feedbacks=[fb])

         res1.save()
         res2.save()

         feedback = self.persistence_delegate.add_responses_to_feedback(1, 
                                                  [res1, res2, res3, res4])

         self.assertEqual(len(feedback.get("responses")), 4)
         self.assertEqual(feedback.get("responses")[0], res1)
         self.assertEqual(feedback.get("responses")[1], res2)
         self.assertEqual(feedback.get("responses")[2], res3)
         self.assertEqual(feedback.get("responses")[3], res4)
         self.assertEqual(len(Answer.get_all()), 4)
         self.assertEqual(len(Question.get_all()), 3)
         self.assertEqual(len(Response.get_all()), 4)

if __name__ == '__main__':
    unittest.main()
