# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from time import sleep
from google.appengine.api.users import get_current_user
from gaebusiness.business import CommandExecutionException
from tekton.gae.middleware.json_middleware import JsonResponse
from question_app import question_facade
from gaepermission.decorator import login_required
from question_app.question_model import CategoryQuestion
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
def edit(_resp, _logged_user, id, **question_properties):
    cmd = question_facade.update_question_cmd(id, **question_properties)
    return _save_or_update_json_response(_logged_user, cmd, _resp)


@login_required
def delete(_resp, id):
    cmd = question_facade.delete_question_cmd(id)
    try:
        cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)


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

