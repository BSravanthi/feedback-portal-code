
# -*- coding: utf-8 -*-
from runtime.utils.type_utils import *
from runtime.utils.class_templates import *
from runtime.exceptions.custom_exceptions import *

Question = ClassTemplate.mk_class("Question")
Answer = ClassTemplate.mk_class("Answer")
Response = ClassTemplate.mk_class("Response")
Feedback = ClassTemplate.mk_class("Feedback")
Session = ClassTemplate.mk_class("Session")

is_question = is_inst(Question)
check_question = check_pred(is_question)

is_answer = is_inst(Answer)
check_answer = check_pred(is_answer)

def are_answers(answers):
    ret_val = True
    if is_list(answers):
        for answer in answers:
            if not is_answer(answer):
                ret_val = False
    else:
        ret_val = False

    return ret_val

is_feedback = is_inst(Feedback)
check_feedback = check_pred(is_feedback)

def are_feedbacks(feedbacks):
    ret_val = True
    if is_list(feedbacks):
        for feedback in feedbacks:
            if not is_feedback(feedback):
                ret_val = False
    else:
        ret_val = False

    return ret_val

is_response = is_inst(Response)
check_response = check_pred(is_response)

def are_responses_or_empty_list(responses):
    ret_val = True
    if is_list(responses): #or responses.__class__.__name__ == 'InstrumentedList':
        for res in responses:
            if not is_response(res):
                ret_val = False
    else:
        ret_val = False

    return ret_val

def are_responses(responses):
    if are_responses_or_empty_list(responses):
        return not responses == []
    else:
        return False

is_session = is_inst(Session)
check_session = check_pred(is_session)

Question.add_attributes(name=is_str, question_type=is_str)
Question.__eq__ = lambda self, other: \
                  isinstance(other, self.__class__) and \
                  self.get("name") == other.get("name")

Answer.add_attributes(name=is_str)
Answer.__eq__ = lambda self, other: \
                  isinstance(other, self.__class__) and \
                  self.get("name") == other.get("name")

Response.add_attributes(question=is_question, 
                        answers=are_answers, 
                        feedbacks=are_feedbacks)

Response.__eq__ = lambda self, other: \
                  isinstance(other, self.__class__) and \
                  self.get("question") == other.get("question") and \
                  self.get("answers") == other.get("answers")

Feedback.add_attributes(gateway_ip=is_str,
                        lab_name=is_str,
                        exp_name=is_str,
                        date=is_date,
                        version=is_str,
                        user_id=is_str,
                        responses=are_responses_or_empty_list)

#Feedback.__eq__ = lambda self, other: \
#                  isinstance(other, self.__class__) and \
#                  self.get("response") == other.get("response")

Session.add_attributes(key=is_str)
Session.__eq__ = lambda self, other: \
                  isinstance(other, self.__class__) and \
                  self.get("key") == other.get("key")
