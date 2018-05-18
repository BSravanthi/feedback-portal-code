
# -*- coding: utf-8 -*-
from runtime.system.system import *
import datetime
from flask import current_app
from runtime.config.feedback_forms import feedback_forms
from runtime.config.system_config import KEY

class SystemInterface ():

    def __init__(self):
        raise Error('Can not instantiate')

    @staticmethod
    def initialize(cls):
        System.initialize_system(cls)

    @staticmethod
    def get_generic_feedback_form(version):
        for feedback_form in feedback_forms:
            if feedback_form['version'] == version:
                current_app.logger.debug("feedback form version %s " %(version))
                return feedback_form

    @staticmethod
    def get_feedback_form(key, lab_name, exp_name, version, user_id):
        try:
            session_cls = System.delegate.entities['session']
            if len(lab_name) == 0:
                lab_name = None
            
            current_app.logger.debug("running operation get_feedback_form")
            questions_dict = System.do("get_feedback_form",
                                           session=session_cls(key=key),
                                           lab_name=lab_name, 
                                           exp_name=exp_name,
                                           version=version,
                                           user_id=user_id)
            current_app.logger.debug("completed operation get_feedback_form")
            return questions_dict

        except (ArityError, TypeError, NotAuthorizedError, StateError) as err:
            current_app.logger.error("%s" %(str(err)))
            raise err

        except Exception as err:
            current_app.logger.error("%s" %(str(err)))
            raise err

    @staticmethod
    def add_feedback(data_dict):
        session_cls = System.delegate.entities['session']
        response_cls = System.delegate.entities['response']
        question_cls = System.delegate.entities['question']
        answer_cls = System.delegate.entities['answer']

        if 'exp_name' not in data_dict:
            data_dict['exp_name'] = "Null"

        if 'user_id' not in data_dict:
            data_dict['user_id'] = "Null"

        if 'date' not in data_dict:
            data_dict['date'] = datetime.datetime.now().date()
            
        responses = data_dict['responses']
        data_dict['responses'] = []
        data_dict['session'] = session_cls(key=data_dict['key'])
        del(data_dict['key'])

        fb = None
        try:
            current_app.logger.debug("running operation add_feedback")
            fb = System.do("add_feedback", **data_dict)
            current_app.logger.debug("completed operation add_feedback")

        except (ArityError, TypeError, NotAuthorizedError, StateError) as err:
            current_app.logger.error("Exception = %s" % str(err))
            raise err

        except Exception as err:
            current_app.logger.error("Exception = %s" % str(err))
            raise err

        response_list = []
        try:
            for response in responses:
                question = question_cls(name=str(response['name']),
                                        question_type="")
                answers = response['answers']
                answer_list = []
                for answer in answers:
                    answer = answer_cls(name=str(answer))
                    answer_list.append(answer)
 
                res = response_cls(question=question, answers=answer_list,
                                    feedbacks=[fb])
                response_list.append(res)
            current_app.logger.debug("running operation add_responses_to_feedback")
            feedback = System.do("add_responses_to_feedback",
                                    responses=response_list,
                                    fb_id=int(fb.id),
                                    session=data_dict['session'])
            current_app.logger.debug("running operation add_responses_to_feedback")
            return feedback
        except Exception as e:
            fb.delete()
            current_app.logger.error("Exception = %s" % str(e))
            raise e

    @staticmethod
    def update_question(data_dict):
        session_cls = System.delegate.entities['session']
        question_cls = System.delegate.entities['question']

        session = session_cls(key=data_dict['key'])
        question = question_cls.get_by_id(data_dict['q_id'])

        if 'name' not in data_dict:
            name=str(question.get("name"))
        else:
            name=data_dict['name']

        if 'question_type' not in data_dict:
            question_type=str(question.get("question_type"))
        else:
            question_type=data_dict['question_type']

        try:
            current_app.logger.debug("running operation update_question")
            question = System.do("update_question", question=question,
                                    name=name, question_type=question_type,
                                    session=session)
            current_app.logger.debug("completed operation update_question")
            return question.to_client()
        except (ArityError, TypeError, NotAuthorizedError, StateError) as err:
            current_app.logger.error("Exception = %s" % str(err))
            raise err

        except Exception as err:
            current_app.logger.error("Exception = %s" % str(err))
            raise err
    @staticmethod
    def delete_question(q_id):
        session_cls = System.delegate.entities['session']

        session = session_cls(key=KEY)
        try:
            current_app.logger.debug("running operation delete_question")
            question = System.do("delete_question", q_id=int(q_id),
                                    session=session)
            current_app.logger.debug("completed operation delete_question")
            return question
        except (ArityError, TypeError, NotAuthorizedError, StateError) as err:
            current_app.logger.error("Exception = %s" % str(err))
            raise err

        except Exception as err:
            current_app.logger.error("Exception = %s" % str(err))
            raise err
    @staticmethod
    def add_generic_feedback(data_dict):
        session_cls = System.delegate.entities['session']
        response_cls = System.delegate.entities['response']
        question_cls = System.delegate.entities['question']
        answer_cls = System.delegate.entities['answer']

        data_dict['session'] = session_cls(key=KEY)
        data_dict['date'] = datetime.datetime.now().date()
        data_dict['user_id'] = "Null"

        if 'lab_name' not in data_dict:
            data_dict['lab_name'] = "generic feedback"

        if 'exp_name' not in data_dict:
            data_dict['exp_name'] = "Null"

            
        responses = data_dict['responses']
        data_dict['responses'] = []

        fb = None
        try:
            current_app.logger.debug("running operation add_feedback")
            fb = System.do("add_feedback", **data_dict)
            current_app.logger.debug("completed operation add_feedback")
        except Exception as err:
            current_app.logger.error("Exception = %s" % str(err))
            raise err

        response_list = []
        try:
            for response in responses:
                question = question_cls(name=str(response['name']),
                                        question_type="")
                answers = response['answers']
                answer_list = []
                for answer in answers:
                    answer = answer_cls(name=str(answer))
                    answer_list.append(answer)
 
                res = response_cls(question=question, answers=answer_list,
                                    feedbacks=[fb])
                response_list.append(res)
            current_app.logger.debug("running operation add_responses_to_feedback")
            feedback = System.do("add_responses_to_feedback",
                                    responses=response_list,
                                    fb_id=int(fb.id),
                                    session=data_dict['session'])
            current_app.logger.debug("completed operation add_responses_to_feedback")
            return feedback
        except Exception as e:
            fb.delete()
            current_app.logger.error("Exception = %s" % str(e))
            raise e

    @staticmethod
    def get_feedback_usage(gateway_ip, new_date, key):
        try:
            current_app.logger.debug("")
            session_cls = System.delegate.entities['session']
            session = session_cls(key=str(key))
        except Exception as e:
            print str(e)
        date = datetime.datetime.strptime(new_date, "%d-%m-%Y").date()
        gateway_ip = str(gateway_ip)
        try:
            current_app.logger.debug("running operation get_feedback_usage")
            usage = System.do("get_feedback_usage",
                                     gateway_ip=gateway_ip,
                                     date=date,
                                     session=session)
            current_app.logger.debug("completed operation get_feedback_usage")
            return usage
        except Exception as e:
            current_app.logger.error("Exception %s" %(str(e)))
            print str(e)

    @staticmethod
    def get_feedback_dump(new_date, key):
        try:
            session_cls = System.delegate.entities['session']
            session = session_cls(key=str(key))
        except Exception as e:
            current_app.logger.error("Exception %s" %(str(e)))
            print str(e)
        date = datetime.datetime.strptime(new_date, "%d-%m-%Y").date()
        try:
            current_app.logger.debug("running operation get_feedback_dump")
            feedbacks = System.do("get_feedback_dump",
                                     date=date,
                                     session=session)
            current_app.logger.debug("completed operation get_feedback_dump")
            feedback_dict_list = []
            for feedback in feedbacks:
                fb_c = feedback.to_client()
                for response in fb_c['responses']:
                    del(response['feedbacks'])

                date_obj = fb_c['date'] 
                date_str = date_obj.strftime('%d-%m-%Y')
                fb_c['date'] = date_str
                feedback_dict_list.append(fb_c)

            return  feedback_dict_list
            
        except Exception as e:
            current_app.logger.error("Exception %s" %(str(e)))
            print str(e)

    @staticmethod
    def add_question(data_dict):
        session_cls = System.delegate.entities['session']
        question_cls = System.delegate.entities['question']

        session = session_cls(key=data_dict['key'])
        question = question_cls(name=data_dict['name'],
                                question_type=data_dict['question_type'])
        try:
            current_app.logger.debug("running operation add_question")
            question = System.do("add_question", question=question, 
                                    session=session)
            current_app.logger.debug("completed operation add_question")
            return question.to_client()
        except (ArityError, TypeError, NotAuthorizedError, StateError) as err:
            current_app.logger.error("Exception = %s" % str(err))
            raise err

        except Exception as err:
            current_app.logger.error("Exception = %s" % str(err))
            raise err
    @staticmethod
    def get_questions():
        question_cls = System.delegate.entities['question']
        try:
            current_app.logger.debug("getting questions")
            questions = question_cls.get_all()
            question_dict_list = []
            for question in questions:
                question_x = question.to_client()
                question_dict_list.append(question_x)
            current_app.logger.debug("got questions")
            return  question_dict_list
        except (ArityError, TypeError, NotAuthorizedError, StateError) as err:
            current_app.logger.error("Exception = %s" % str(err))
            raise err

        except Exception as err:
            current_app.logger.error("Exception = %s" % str(err))
            raise err
    @staticmethod
    def get_question_by_id(id):
        question_cls = System.delegate.entities['question']
        try:
            current_app.logger.debug("getting question by id")
            question = question_cls.get_by_id(id)
            if not question:
                return ("No question found with id: %s" % (id))

            return question.to_client()

        except (ArityError, TypeError, NotAuthorizedError, StateError) as err:
            current_app.logger.error("Exception = %s" % str(err))
            raise err

        except Exception as err:
            current_app.logger.error("Exception = %s" % str(err))
            raise err
