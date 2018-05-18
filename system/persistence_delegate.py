
# -*- coding: utf-8 -*-
from runtime.persistence.entities import *
from runtime.exceptions.custom_exceptions import *
from flask import current_app

class PersistenceDelegate():
   
    def __init__(self):
        self.entities = {'session': Session,
                         'question': Question,
                         'answer': Answer,
                         'response': Response,
                         'feedback': Feedback
                        }


    def get_object(self, cls, **kwargs):
        ret_val = None
        try:
            ret_val = cls.apply_filters(**kwargs)[0]
        except NotFoundError as e:
            ret_val = None
        
        return ret_val

    def get_question(self, **kwargs):
        current_app.logger.debug("")
        return self.get_object(Question, **kwargs)

    def get_answer(self, **kwargs):
        current_app.logger.debug("")
        return self.get_object(Answer, **kwargs)

    def get_responses(self, **kwargs):
        current_app.logger.debug("")
        responses = []
        if "question" in kwargs.keys() and len(kwargs.keys()) == 1:
            try:
                responses = Response.apply_filters(**kwargs)
            except NotFoundError as e:
                pass
            except Exception as e:
                pass
        
        return responses

    def get_response(self, **args):
        current_app.logger.debug("")
        # ret_val = None
        # if "question" in args.keys() and "answers" in args.keys():
        #     question = args["question"]
        #     answers = args["answers"]
        #     responses = self.get_responses(question=question)
        #     if responses:

        #         def equality_of_response(response):
        #             response_answers = response.get("answers")
        #             if (len(response_answers) == len(answers) and
        #                     sorted(response_answers) == sorted(answers)):
        #                 return True
        #             else:
        #                 return False
                    
        #         filtered_responses = filter(equality_of_response, responses)

        #         if filtered_responses:
        #             ret_val = filtered_responses[0]

        # return ret_val

        ret_val = None

        def equality(responses, answers):
            ret_val = None

            for response in responses:
                loop_val = True
                s_r_a = sorted(response.get("answers"))
                s_a = sorted(answers)

                if len(s_r_a) != len(s_a):
                    continue

                for val in s_r_a:
                    if val not in s_a:
                        loop_val = False
                        break

                    if loop_val:
                        ret_val = response
                        break
                    else:
                        continue

            return ret_val
        
        if "question" in args.keys() and "answers" in args.keys():
            question = args["question"]
            answers = args["answers"]
            responses = self.get_responses(question=question)
            if responses:
                ret_val = equality(responses, answers)

        return ret_val

    def question_exists(self, question):
        current_app.logger.debug("")
        question_name = question.get("name")
        return question == self.get_question(name=question_name)
        
    def answer_exists(self, answer):
        current_app.logger.debug("")
        answer_name = answer.get("name")
        return answer == self.get_answer(name=answer_name)
        
    def feedback_exists(self, fb_id):
        ret_val = False
        current_app.logger.debug("")
        try:
            if Feedback.get_by_id(fb_id) is not None:
                ret_val = True
        except Exception as e:
            pass

        return ret_val 
        
    def response_exists(self, response):
        current_app.logger.debug("")
        ret_val_dict = {'exists' : False,
                        'value' : None
                       }
        
        question = response.get("question")
        answers = response.get("answers")
        response = self.get_response(question=question, answers=answers)
        if response is not None:
            ret_val_dict['exists'] = True
            ret_val_dict['value'] = response

        return ret_val_dict


    def add_question(self, question):
        current_app.logger.debug("")
        question.save()
        return question

    def delete_question(self, q_id):
        record = Question.get_by_id(q_id)
        current_app.logger.debug("")
        if not record:
            abort(404, 'No question with id %s' % (q_id))
        else:
            try:
                record.delete()
                #db.session.delete(record)
                #db.session.commit()
            except Exception, e:
                print e
                abort(500, str(e))

        return q_id

    def add_answer(self, answer):
        current_app.logger.debug("")
        answer.save()
        return answer

    def add_feedback(self, gateway_ip, lab_name, exp_name, date,
                         version, user_id, responses):
        try:
            current_app.logger.debug("")
            new_feedback = Feedback(gateway_ip=gateway_ip,
                                    lab_name=lab_name,
                                    exp_name=exp_name,
                                    date=date,
                                    version=version,
                                    user_id=user_id,
                                    responses=responses)
            new_feedback.save()
            return new_feedback
        except Exception as err:
            current_app.logger.error("Exception = %s" % str(err))
            raise err

    def update_question(self, question, name, question_type):
        current_app.logger.debug("")
        question.set(name=name, question_type=question_type)
        question.save()
        return question

    def get_feedbacks(self, **kwargs):
        current_app.logger.debug("")
        ret_val = None
        try:
            ret_val = Feedback.apply_filters(**kwargs)
        except NotFoundError as e:
            ret_val = None
        
        return ret_val

    def get_feedback_by_id(self, id):
        current_app.logger.debug("")
        ret_val = None
        try:
            ret_val = Feedback.get_by_id(id)
        except Exception as err:
            current_app.logger.error("Exception = %s" % str(err))
            ret_val = None
        
        return ret_val

    def get_feedback_usage(self, gateway_ip, date):
        current_app.logger.debug("")
        try:
            feedbacks = self.get_feedbacks(gateway_ip=gateway_ip, date=date)
            return len(feedbacks)
        except Exception as e:
            print "no feedback found with given ip %s and date %s" \
              %(gateway_ip, date)

    def get_feedback_dump(self, date):
        current_app.logger.debug("")
        try:
            feedbacks = self.get_feedbacks(date=date)
            return feedbacks
        except Exception as e:
            print "no feedbacks were found on date %s" \
              %(date)

    def add_responses_to_feedback(self, fb_id, responses):
        current_app.logger.debug("")
        feedback = self.get_feedback_by_id(fb_id)
        response_list = []
        for response in responses:
            answers = response.get("answers")
            ret_val_dict = self.response_exists(response)
            if ret_val_dict['exists']:
                response = ret_val_dict['value']
            else:
                answer_list = []
                for answer in answers:
                    if self.answer_exists(answer):
                        answer = self.get_answer(name=answer.get("name"))
                    else:
                        answer.save()
                    answer_list.append(answer)
                question = response.get("question")
                question = self.get_question(name=question.get("name"))
                response.set(question=question, answers=answer_list,
                                 feedbacks=[feedback])

            response_list.append(response)

        feedback.set(responses=response_list)
        return feedback
