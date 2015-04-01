# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from my_discusses_app.utils import FriendlyDatetime
from question_app import question_facade
from datetime import datetime
from gaepermission.model import MainUser
from tekton import router
from routes.comments.rest import new as comment_path

allowed = "python business-intelligence geo-technology mongodb c++ agile artificial-intelligence scidb".split()


@no_csrf
def index(category=""):
    if category:
        if category not in allowed:
            return TemplateResponse(template_path="base/404.html")
        topics = [
            {
                "key": 54323122,
                "title": "Who Invented the Computer Virus?",
                "content": "",
                "image": "/static/img/python.jpg",
                "type": "questions",
                "user": 1235875214
            },
            {
                "key": 65432322,
                "title": "How to Google Something You Don't Know How to Describe?",
                "content": "",
                "image": "/static/img/test.jpg",
                "type": "discusses",
                "user": 54389754354
            }
        ]
        context = {"category": category, "topics": topics}
        return TemplateResponse(context=context, template_path="category/home.html")
    formatter = FriendlyDatetime()
    cmd = question_facade.list_questions_cmd()
    questions = cmd()
    qform = question_facade.question_form()

    def localize_user(question):
        question_dct = qform.fill_with_model(question)
        question_dct['user'] = MainUser.get_by_id(int(question.user.id()))
        question.created_at = datetime.now() - question.creation
        print question_dct
        return question_dct
    questions_output = [localize_user(q) for q in questions]

    context = {
        "questions": questions_output,
        "question_comment_path": router.to_path(comment_path),
        "discuss_comment_path": router.to_path(comment_path),
        "users_path": router.to_path(index),
        "trends": [
            {
                "key": 54323122,
                "title": "Who Invented the Computer Virus?",
                "content": "",
                "image": "/static/img/python.jpg",
                "type": "questions",
                "user": 54389754354,
                "creation": formatter(datetime(day=10, month=3, year=2015, hour=8))
            },
            {
                "key": 65432322,
                "title": "How to Google Something You Don't Know How to Describe?",
                "content": "",
                "image": "/static/img/test.jpg",
                "type": "discusses",
                "user": 1235875214,
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

