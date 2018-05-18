
# -*- coding: utf-8 -*-

from runtime.exceptions.custom_exceptions import *
from runtime.objects.entities import is_str, is_question, is_answer, \
     is_feedback, is_date, is_response, is_session, are_responses, is_int,\
     are_responses_or_empty_list
from runtime.utils.type_utils import is_str_or_none
from runtime.config.system_config import KEY
from runtime.config.feedback_forms import feedback_forms
import datetime
from flask import current_app

class System ():

    def __init__(self):
        raise Error('Can not instantiate')

    @staticmethod
    def initialize_system(cls):
        System.delegate = cls()

    @staticmethod
    def is_session_valid(session):
        return session.get("key") == KEY
 
   
    @staticmethod
    def arity_check(args, n):
       if  (len(args) != n) :
          raise ArityError("arity mismatch: size of args  does not " + 
                           "match operation arity " )

    @staticmethod
    def type_check(args, arg_types):
        for key, value in args.iteritems():
            if not arg_types[key](value):
                raise TypeError("type mismatch: argument %s is not of "
                                "type %s" % (value, key))

    @staticmethod   
    def do(op, **args):
        cls = ops_table[op]
        arg_types  = cls.arg_types
        auth_check = cls.auth_check
        state_check = cls.state_check
        arity_and_type_checks_needed = cls.arity_and_type_checks_needed
        try:
            if arity_and_type_checks_needed:
               System.arity_check(args.keys(), len(arg_types.keys()))
               System.type_check(args, arg_types)
            auth_check(args)
            state_check(args)
            return cls.action(args)
        except (ArityError, TypeError, NotAuthorizedError, StateError) as err:
            raise err

class AddQuestion():
    arg_types = {"question": is_question, "session": is_session}
    arity_and_type_checks_needed = True

    @staticmethod
    def auth_check(args):
        session = args['session']
        current_app.logger.debug("checking authorization")
        if not System.is_session_valid(session):
            current_app.logger.debug("authorization is failed")
            raise NotAuthorizedError("Not Authorized to perform this action")
        current_app.logger.debug("authorization check is done")
    @staticmethod
    def state_check(args):
        question = args["question"]
        current_app.logger.debug("checking state")
        if System.delegate.question_exists(question):
            current_app.logger.debug("state check is failed")
            raise StateError("question %s already exists in System"
                                 % question.to_client())
        current_app.logger.debug("state check is done")
    @staticmethod
    def action(args):
        question = args["question"]
        current_app.logger.debug("running delegate.add_question")
        question = System.delegate.add_question(question)
        current_app.logger.debug("completed delegate.add_question")
        return question

class UpdateQuestion():
    arg_types = {"question": is_question, "name": is_str,
                     "question_type": is_str,
                     "session": is_session}
    arity_and_type_checks_needed = True

    @staticmethod
    def auth_check(args):
        session = args['session']
        current_app.logger.debug("checking authorization")
        if not System.is_session_valid(session):
            current_app.logger.debug("authorization is failed")
            raise NotAuthorizedError("Not Authorized to perform this action")
        current_app.logger.debug("authorization check is done")
    @staticmethod
    def state_check(args):
        pass

    @staticmethod
    def action(args):
        question = args["question"]
        name = args["name"]
        question_type = args["question_type"]
        current_app.logger.debug("running delegate.update_question")
        question = System.delegate.update_question(question, name,\
            question_type)
        current_app.logger.debug("completed delegate.update_question")
        return question

class DeleteQuestion():
    arg_types = {"q_id": is_int, "session": is_session}
    arity_and_type_checks_needed = True

    @staticmethod
    def auth_check(args):
        session = args['session']
        current_app.logger.debug("checking authorization")
        if not System.is_session_valid(session):
            current_app.logger.debug("authorization is failed")
            raise NotAuthorizedError("Not Authorized to perform this action")

    @staticmethod
    def state_check(args):
        pass

    @staticmethod
    def action(args):
        q_id = args["q_id"]
        current_app.logger.debug("running delegate.delete_question")
        q_id = System.delegate.delete_question(q_id)
        current_app.logger.debug("completed delegate.delete_question")
        return q_id

class AddAnswer():
    arg_types = {"answer": is_answer, "session": is_session}
    arity_and_type_checks_needed = True

    @staticmethod
    def auth_check(args):
        session = args['session']
        current_app.logger.debug("checking authorization")
        if not System.is_session_valid(session):
            current_app.logger.debug("authorization is failed")
            raise NotAuthorizedError("Not Authorized to perform this action")

    @staticmethod
    def state_check(args):
        answer = args["answer"]
        current_app.logger.debug("checking state")
        if System.delegate.answer_exists(answer):
            current_app.logger.debug("state check is failed")
            raise StateError("answer %s already exists in System"
                                 % answer.to_client())
        current_app.logger.debug("state check is done")
    @staticmethod
    def action(args):
        answer = args["answer"]
        current_app.logger.debug("running delegate.add_answer")
        answer = System.delegate.add_answer(answer)
        current_app.logger.debug("completed delegate.add_answer")
        return answer

class AddFeedback():
    arg_types = {"gateway_ip": is_str, "lab_name": is_str, "date": is_date,
                  "exp_name": is_str, "responses": are_responses_or_empty_list,
                  "version": is_str, "user_id": is_str, "session": is_session}
    arity_and_type_checks_needed = True

    @staticmethod
    def auth_check(args):
        session = args['session']
        current_app.logger.debug("checking authorization")
        if not System.is_session_valid(session):
            current_app.logger.error("auth error raised, session = %s" % 
                                        session.to_client())
            raise NotAuthorizedError("Not Authorized to perform this action")
        current_app.logger.debug("authorization check is done")
    @staticmethod
    def state_check(args):
        pass

    @staticmethod
    def action(args):
        gateway_ip = args["gateway_ip"]
        lab_name = args["lab_name"]
        exp_name = args["exp_name"]
        date = args["date"]
        version = args["version"]
        user_id = args["user_id"]
        responses = args['responses']
        try:
            current_app.logger.debug("running delegate.add_feedback")
            feedback = System.delegate.add_feedback(gateway_ip, 
                                                        lab_name,
                                                        exp_name,
                                                        date,
                                                        version,
                                                        user_id,
                                                        responses)
            current_app.logger.debug("completed delegate.add_feedback")
            return feedback
        except Exception as err:
            current_app.logger.error("Exception = %s" % str(err))
            raise err

class GetFeedbackUsage():
    arg_types = {"gateway_ip": is_str, "date": is_date,
                  "session": is_session}
    arity_and_type_checks_needed = True

    @staticmethod
    def auth_check(args):
        session = args['session']
        current_app.logger.debug("checking authorization")
        if not System.is_session_valid(session):
            current_app.logger.debug("authorization is failed")
            raise NotAuthorizedError("Not Authorized to perform this action")
        current_app.logger.debug("authorization check is done")
    @staticmethod
    def state_check(args):
        pass

    @staticmethod
    def action(args):
        gateway_ip = args["gateway_ip"]
        date = args["date"]
        current_app.logger.debug("running delegate.get_feedback_usage")
        usage = System.delegate.get_feedback_usage(gateway_ip, date) 
        current_app.logger.debug("completed delegate.get_feedback_usage")
        return usage

class GetFeedbackDump():
    arg_types = {"date": is_date, "session": is_session}
    arity_and_type_checks_needed = True

    @staticmethod
    def auth_check(args):
        session = args['session']
        current_app.logger.debug("checking authorization")
        if not System.is_session_valid(session):
            current_app.logger.debug("authorization is failed")
            raise NotAuthorizedError("Not Authorized to perform this action")
        current_app.logger.debug("authorization check is done")

    @staticmethod
    def state_check(args):
        pass

    @staticmethod
    def action(args):
        date = args["date"]
        current_app.logger.debug("running delegate.get_feedback_dump")
        feedbacks = System.delegate.get_feedback_dump(date) 
        current_app.logger.debug("completed delegate.get_feedback_dump")
        return feedbacks

class AddResponsesToFeedback():
    arg_types = {"responses": are_responses, "fb_id": is_int, 
                     "session": is_session}
    arity_and_type_checks_needed = True

    @staticmethod
    def auth_check(args):
        session = args['session']
        current_app.logger.debug("checking authorization")
        if not System.is_session_valid(session):
            current_app.logger.error("auth error raised, session = %s" % 
                                        session.to_client())
            raise NotAuthorizedError("Not Authorized to perform this action")
        current_app.logger.debug("authorization check is done")
    @staticmethod
    def state_check(args):
        fb_id = args["fb_id"]
        current_app.logger.debug("checking state")
        if not System.delegate.feedback_exists(fb_id):
            current_app.logger.error("feedback with id = %d does not exist"
                                     " in System" % fb_id)
            raise StateError("feedback with id = %d does not exist in System"
                                 % fb_id)
        current_app.logger.debug("state check is done")
    @staticmethod
    def action(args):
        fb_id = args["fb_id"]
        responses = args["responses"]
        try:
            current_app.logger.debug("running delegate.add_response_to_feedback")
            feedback = System.delegate.add_responses_to_feedback(fb_id, 
                                                                 responses)
            current_app.logger.debug("completed delegate.add_response_to_feedback")
            return feedback
        except Exception as err:
            current_app.logger.error("Exception = %s" % str(err))
            raise err

class GetFeedbackForm():
    arg_types = {"session": is_session,
                 "lab_name": is_str,
                 "exp_name": is_str_or_none,
                 "version": is_str_or_none,
                 "user_id": is_str_or_none}

    arity_and_type_checks_needed = True

    @staticmethod
    def auth_check(args):
        session = args['session']
        current_app.logger.debug("checking authorization")
        if not System.is_session_valid(session):
            current_app.logger.debug("authorization is failed")
            raise NotAuthorizedError("Not Authorized to perform this action")
        current_app.logger.debug("authorization check is done")

    @staticmethod
    def state_check(args):
        pass

    @staticmethod
    def action(args):
        return_val  = None
        if args['version'] == None:
            if args['exp_name'] == None:
                return_val = feedback_forms[1]
            else:
                return_val = feedback_forms[0]
                return_val['exp_name'] = args['exp_name']

        return_val['lab_name'] = args['lab_name']
        return_val['key'] = KEY
        if args['user_id'] is not None:
            return_val['user_id'] = args['user_id']

        return return_val

ops_table = {'add_question' : AddQuestion,
             'delete_question': DeleteQuestion,
             'update_question': UpdateQuestion,
             'add_answer' : AddAnswer,
             'add_feedback': AddFeedback,
             'get_feedback_usage': GetFeedbackUsage,
             'get_feedback_dump': GetFeedbackDump,
             'add_responses_to_feedback': AddResponsesToFeedback,
             'get_feedback_form': GetFeedbackForm
            }
