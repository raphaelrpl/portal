# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaecookie.decorator import no_csrf
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


def delete(_resp, identifier):
    print(identifier)
    k = ndb.Key('Comment', identifier)
    cmd = comment_facade.delete_comment_cmd(k)
    try:
        cmd()
    except CommandExecutionException:
        # _resp.status_code = 500
        return JsonResponse(cmd.errors)

def edit(_resp, _logged_user, **comment_properties):
    comment_id = int(comment_properties.get('id'))
    k = ndb.Key('Comment', comment_id)
    if int(_logged_user.key.id()) != int(comment_properties.get('publisher', {}).get('id', 0)) and comment_id != None:
        _resp.status_code = 400
        return JsonResponse({"content": "This post don't belong to you!"})
    comment = Comment.get_by_id(k.id())

    try:
        if comment_properties.get('content') is None or comment_properties.get('content') == "":
            raise ValueError()
        comment.content = comment_properties.get('content')
        form = comment_facade.comment_form()
        form_data = form.fill_with_model(comment)
        comment.put()
    except Exception as e:
        _resp.status_code = 400
        return JsonResponse({"content": "Required field"})
    return JsonResponse(form_data)
    # cmd = comment_facade.update_comment_cmd(k, **comment_properties)
    # return _save_or_update_json_response(cmd, _resp)


def _save_or_update_json_response(cmd, _resp):
    try:
        comment = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    comment_form = comment_facade.comment_form()
    return JsonResponse(comment_form.fill_with_model(comment))

