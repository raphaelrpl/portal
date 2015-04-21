# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from question_app import question_facade
from routes.questions import new, edit
from tekton.gae.middleware.redirect import RedirectResponse
from gaepermission.model import MainUser
from datetime import datetime
from routes.comments.rest import new as comment_new, index as comment_list
from comment_app import comment_facade
from comment_app.comment_model import Comment
from permission_app.permission_facade import main_user_form
from json import dumps


@no_csrf
def index(question_id=""):
    if question_id:
        cmd = question_facade.get_question_cmd(question_id)
        question = cmd()
        form = question_facade.question_form()
        if not question:
            return RedirectResponse(index)
        question_dct = form.fill_with_model(question)
        question_dct['publisher'] = MainUser.get_by_id(question_dct['user'])

        comment_form = comment_facade.comment_form()
        comments_on_question = Comment.filter_by_question_key(question.key).fetch()

        def fill_comment_model(comment):
            comment_dct = comment_form.fill_with_model(comment)
            comment_dct['publisher'] = main_user_form().fill_with_model(MainUser.get_by_id(int(question_dct['user'])))
            return comment_dct

        comments = [fill_comment_model(c) for c in comments_on_question]

        context = {
            "question": question_dct,
            "comments": dumps(comments),
            "comment_url": router.to_path(comment_new),
            "comment_list": router.to_path(comment_list)}
        return TemplateResponse(context=context, template_path='questions/question.html')
    cmd = question_facade.list_questions_cmd()
    questions = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    question_form = question_facade.question_form()

    def localize_question(question):
        question_dct = question_form.fill_with_model(question)
        question_dct['publisher'] = MainUser.get_by_id(question_dct['user'])
        question_dct['edit_path'] = router.to_path(edit_path, question_dct['id'])
        question_dct['delete_path'] = router.to_path(delete_path, question_dct['id'])
        return question_dct

    localized_questions = [localize_question(question) for question in questions][::-1]
    query = [
        {
            "id": 318463,
            "name": "Lorem Ipsum San Shi",
            "user": 8236478523,
            "creation": datetime.now() - datetime.now(),
        },
        {
            "id": 318433,
            "name": "Lorem Ipsum San Shi",
            "user": 8236423442,
            "creation": datetime.now() - datetime.now(),
        }
    ]
    context = {'questions': localized_questions,
               'new_path': router.to_path(new),
               'question_path': router.to_path(index)}
    return TemplateResponse(context, template_path='questions/home.html')


def delete(question_id):
    question_facade.delete_question_cmd(question_id)()
    return RedirectResponse(router.to_path(index))

