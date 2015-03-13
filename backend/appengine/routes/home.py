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
def index():
    # cmd = question_facade.list_questions_cmd()
    # questions = cmd()
    #
    # question_form = question_facade.question_form()
    formatter = FriendlyDatetime()
    #
    # output = [question_form.fill_with_model(data) for data in questions]
    questions = Question.query().order(Question.creation).fetch()[:10][::-1]

    for question in questions:
        question.created_at = datetime.now() - question.creation
    context = {
        # "questions": dumps(output),
        "questions": questions,
        "discusses": [
            {
                "title": "Quais os principais assuntos no tutorship portal?",
                "content": "",
                "image": "/static/img/python.jpg",
                "creation": formatter(datetime(day=10, month=3, year=2015, hour=8))
            },
            {
                "title": "Quais os principais assuntos no tutorship portal?",
                "content": "",
                "image": "/static/img/test.jpg",
                "creation": formatter(datetime(day=9, month=3, year=2015, hour=8))
            }
        ]
    }
    return TemplateResponse(context=context)

