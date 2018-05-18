
# -*- coding: utf-8 -*-
from runtime.objects.entities import *
from runtime.utils.class_persistence_template import *
import datetime

args = {"__tablename__": "question",
        "id": db.Column(db.Integer, primary_key=True),
        "name": db.Column(db.String(255), unique=True, nullable=False),
        "question_type": db.Column(db.String(255), unique=False, 
                                       nullable=True),
        "responses": db.relationship('Response', 
                                        backref=db.backref('question'))
        }

Question = ClassPersistenceTemplate.mk_persistent(Question, ['name'], **args)

args = {"__tablename__": "answer",
        "id": db.Column(db.Integer, primary_key=True),
        "name": db.Column(db.String(255), unique=True, nullable=False)
        }

Answer = ClassPersistenceTemplate.mk_persistent(Answer, ['name'], **args)

args = {"__tablename__": "feedback",
        "id": db.Column(db.Integer, primary_key=True),
        "gateway_ip" : db.Column(db.String(255), nullable=False),
        "lab_name" : db.Column(db.String(255), nullable=False),
        "exp_name" : db.Column(db.String(255), nullable=True),
        "user_id" : db.Column(db.String(255), nullable=True),
        "version" : db.Column(db.String(255), nullable=False),
        "date": db.Column(db.Date, nullable=False)
        }

Feedback = ClassPersistenceTemplate.mk_persistent(Feedback, [], **args)

responses_answers = db.Table('responses_answers',
		      db.Column('response_id', db.Integer, 
                            db.ForeignKey('response.id')),
		      db.Column('answer_id', db.Integer,
                            db.ForeignKey('answer.id')))

responses_feedbacks = db.Table('responses_feedbacks',
		      db.Column('response_id', db.Integer, 
                            db.ForeignKey('response.id')),
		      db.Column('feedback_id', db.Integer,
                            db.ForeignKey('feedback.id')))

args = {"__tablename__": "response",
        "id": db.Column(db.Integer, primary_key=True),
        "question_id": db.Column(db.Integer, 
                                      db.ForeignKey('question.id'), 
                                      unique=False, nullable=False),

        "feedbacks": db.relationship('Feedback',
                                       secondary=responses_feedbacks, 
                                       backref='responses'),

        "answers": db.relationship('Answer',
                                       secondary=responses_answers, 
                                       backref='responses')
      }

Response = ClassPersistenceTemplate.mk_persistent(Response, 
                                   ['question', 'answers'], **args)
