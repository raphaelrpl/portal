# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaecookie.decorator import no_csrf
from gaebusiness.business import CommandExecutionException
from tekton import router
from permission_app.permission_facade import main_user_form
from tekton.gae.middleware.json_middleware import JsonResponse
from comment_app import comment_facade
from comment_app.comment_model import Comment
from question_app.question_model import Question
from discuss_app.discuss_model import Discuss
from gaepermission.decorator import login_required
from base_app.model import BasePost


@login_required
@no_csrf
def index(post_id=None):
    def localize_user(model, form):
        dct = form.fill_with_model(model)
        dct['publisher'] = main_user_form().fill_with_model(model.user.get())
        dct['user'] = dct['publisher']
        return dct

    if post_id:
        key = ndb.Key(BasePost, int(post_id)).get()
        if key is None:
            return JsonResponse([])
        comments = Comment.query(Comment.post == key.key).fetch()
        if not comments:
            return JsonResponse([])

        comments_dcts = [localize_user(m, comment_facade.comment_form()) for m in comments]
        return JsonResponse(comments_dcts)

    comment_list = Comment.query().fetch()
    comment_form = comment_facade.comment_form()
    comment_dcts = [localize_user(m, comment_form) for m in comment_list]
    return JsonResponse(comment_dcts)


@login_required
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
    return _save_or_update_json_response(_logged_user, cmd, _resp)


@login_required
def delete(_resp, identifier):
    k = ndb.Key('Comment', int(identifier))
    # cmd = comment_facade.delete_comment_cmd(identifier)
    comment = Comment.get_by_id(int(identifier))
    form = comment_facade.comment_form()

    # out = comment
    try:
        comment.key.delete()
    except Exception as e:
        _resp.status_code = 400
        return JsonResponse({"content": "Cannot delete"})
    return JsonResponse(form.fill_with_model(comment))


@login_required
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


def _save_or_update_json_response(_logged_user, cmd, _resp):
    try:
        comment = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    comment_form = comment_facade.comment_form()
    user_form = main_user_form().fill_with_model(_logged_user)
    comment_dc = comment_form.fill_with_model(comment)
    comment_dc['publisher'] = user_form
    comment_dc['delete_path'] = router.to_path(delete, comment_dc['id'])

    return JsonResponse(comment_dc)

