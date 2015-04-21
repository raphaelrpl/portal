# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from question_app import question_facade
from gaebusiness.business import CommandExecutionException
from gaepermission.model import MainUser
from permission_app.permission_facade import main_user_form
from tekton.gae.middleware.json_middleware import JsonResponse
from comment_app import comment_facade
from comment_app.comment_model import Comment
from question_app.question_model import Question
from discuss_app.discuss_model import Discuss


def index(question_id):
    # cmd_question = question_facade.get_question_cmd(question_id)
    # question = cmd_question()

    cmd = comment_facade.list_comments_cmd()
    comment_list = cmd()
    comment_form = comment_facade.comment_form()
    comment_dcts = [comment_form.fill_with_model(m) for m in comment_list]

    # comments_on_question = Comment.filter_by_question_key(question.key).fetch()
    #
    # def fill_comment_model(comment):
    #     comment_dct = comment_form.fill_with_model(comment)
    #     comment_dct['publisher'] = main_user_form().fill_with_model(MainUser.get_by_id(int(question_dct['user'])))
    #     return comment_dct
    #
    # comments = [fill_comment_model(c) for c in comments_on_question]
    return JsonResponse(comment_dcts)


def new(_resp, _logged_user, **comment_properties):
    post = None
    if comment_properties.get('type', '').lower() == 'q':
        # QUESTION
        post = Question.get_by_id(int(comment_properties.get('post')))
    elif comment_properties.get('type', '').lower() == 'd':
        post = Discuss.get_by_id(int(comment_properties.get('post')))
    if post:
        comment_properties['post'] = post
    comment_properties['user'] = _logged_user
    cmd = comment_facade.save_comment_cmd(**comment_properties)
    return _save_or_update_json_response(cmd, _resp)


def edit(_resp, id, **comment_properties):
    cmd = comment_facade.update_comment_cmd(id, **comment_properties)
    return _save_or_update_json_response(cmd, _resp)


def delete(_resp, id):
    cmd = comment_facade.delete_comment_cmd(id)
    try:
        cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)


def _save_or_update_json_response(cmd, _resp):
    try:
        comment = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    comment_form = comment_facade.comment_form()
    return JsonResponse(comment_form.fill_with_model(comment))

