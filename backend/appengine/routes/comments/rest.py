# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from tekton.gae.middleware.json_middleware import JsonResponse
from comment_app import comment_facade


def index():
    cmd = comment_facade.list_comments_cmd()
    comment_list = cmd()
    comment_form = comment_facade.comment_form()
    comment_dcts = [comment_form.fill_with_model(m) for m in comment_list]
    return JsonResponse(comment_dcts)


def new(_resp, **comment_properties):
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

