# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required, login_required
from datetime import datetime
from discuss_app.utils import FriendlyDatetime
from question_app.question_model import Question
from datetime import datetime
from question_app import question_facade
from json import dumps


@login_not_required
@no_csrf
def index(category=""):
    if category:
        topics = [
            {
                "key": 54323122,
                "title": "Who Invented the Computer Virus?",
                "content": "",
                "image": "/static/img/python.jpg",
                "type": "questions",
            },
            {
                "key": 65432322,
                "title": "How to Google Something You Don't Know How to Describe?",
                "content": "",
                "image": "/static/img/test.jpg",
                "type": "discusses",
            }
        ]
        context = {"category": category, "topics": topics}
        return TemplateResponse(context=context, template_path="category/home.html")
    formatter = FriendlyDatetime()
    questions = Question.query().order(Question.creation).fetch()[:10][::-1]

    for question in questions:
        question.created_at = datetime.now() - question.creation
    context = {
        "questions": questions,
        "trends": [
            {
                "key": 54323122,
                "title": "Who Invented the Computer Virus?",
                "content": "",
                "image": "/static/img/python.jpg",
                "type": "questions",
                "creation": formatter(datetime(day=10, month=3, year=2015, hour=8))
            },
            {
                "key": 65432322,
                "title": "How to Google Something You Don't Know How to Describe?",
                "content": "",
                "image": "/static/img/test.jpg",
                "type": "discusses",
                "creation": formatter(datetime(day=9, month=3, year=2015, hour=8))
            }
        ],
        "discusses": [
            {
                "key": 50903412,
                "title": "Quais os principais assuntos no tutorship portal?",
                "content": "",
                "image": "/static/img/python.jpg",
                "creation": formatter(datetime(day=10, month=3, year=2015, hour=8))
            },
            {
                "key": 50903417,
                "title": "Quais os principais assuntos no tutorship portal?",
                "content": "",
                "image": "/static/img/test.jpg",
                "creation": formatter(datetime(day=9, month=3, year=2015, hour=8))
            }
        ]
    }
    return TemplateResponse(context=context)

