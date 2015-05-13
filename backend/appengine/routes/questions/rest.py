# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from time import sleep
from google.appengine.ext import ndb
from gaebusiness.business import CommandExecutionException
from permission_app.permission_facade import main_user_form
from tekton.gae.middleware.json_middleware import JsonResponse
from question_app import question_facade
from gaepermission.decorator import login_required
from question_app.question_model import CategoryQuestion, Question
from category_app.category_model import Category


@login_required
def index():
    cmd = question_facade.list_questions_cmd()
    question_list = cmd()
    question_form = question_facade.question_form()
    question_dcts = [question_form.fill_with_model(m) for m in question_list]
    return JsonResponse(question_dcts)


@login_required
def new(_resp, _logged_user, **question_properties):
    if _logged_user is None:
        _resp.status_code = 400
        return JsonResponse({"name": "Login required!"})
    question_properties['question']['user'] = _logged_user
    # question_properties['user'] = _logged_user
    cmd = question_facade.save_question_cmd(**question_properties.get('question', {}))
    # cmd = question_facade.save_question_cmd(**question_properties)
    try:
        question = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)

    for c in question_properties.get("categorys"):
        cat = Category.query(Category.name == c).fetch()
        if cat:
            category = CategoryQuestion(origin=cat[0], destination=question)
            category.put()

    question_form = question_facade.question_form()
    data = question_form.fill_with_model(question)
    data['user'] = _logged_user.name
    sleep(0.5)

    return JsonResponse(data)


@login_required
def edit(_resp, _logged_user, **question_properties):
    question_id = question_properties.get('id')
    # key = ndb.Key('Question', int(question_id))
    question = Question.get_by_id(int(question_id))

    if int(_logged_user.key.id()) != int(question_properties.get('user', {}).get('id', 0)) and question_id != None:
        _resp.status_code = 400
        return JsonResponse({"name": "This post don't belong to you!"})
    if question is None:
        _resp.status_code = 400
        return JsonResponse({"name": "Invalid post"})

    question.name = question_properties.get('name')
    try:
        question.put()
    except:
        _resp.status_code = 400
        return JsonResponse({"name": "Put a valid question"})
    user_form = main_user_form()
    form = question_facade.question_form()
    question_dct = form.fill_with_model(question)
    question_dct['user'] = user_form.fill_with_model(question.user.get())
    return JsonResponse(question_dct)
    # cmd = question_facade.update_question_cmd(question_id, **question_properties)
    # return _save_or_update_json_response(_logged_user, cmd, _resp)


@login_required
def delete(_resp, id):
    cmd = question_facade.delete_question_cmd(id)
    try:
        question = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    question_dct = question_facade.question_form().fill_with_model(question)
    return JsonResponse(question_dct)


def _save_or_update_json_response(_logged_user, cmd, _resp):
    try:
        question = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    question_form = question_facade.question_form()
    data = question_form.fill_with_model(question)
    data['user'] = _logged_user.name
    return JsonResponse(data)

