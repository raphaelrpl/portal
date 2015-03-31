# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from tekton.gae.middleware.json_middleware import JsonResponse
from discuss_app import discuss_facade


def index():
    cmd = discuss_facade.list_discusss_cmd()
    discuss_list = cmd()
    discuss_form = discuss_facade.discuss_form()
    discuss_dcts = [discuss_form.fill_with_model(m) for m in discuss_list]
    return JsonResponse(discuss_dcts)


def new(_resp, **discuss_properties):
    print "DISCUSSS --> "
    print discuss_properties
    cmd = discuss_facade.save_discuss_cmd(**discuss_properties)
    return _save_or_update_json_response(cmd, _resp)


def edit(_resp, id, **discuss_properties):
    cmd = discuss_facade.update_discuss_cmd(id, **discuss_properties)
    return _save_or_update_json_response(cmd, _resp)


def delete(_resp, id):
    cmd = discuss_facade.delete_discuss_cmd(id)
    try:
        cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)


def _save_or_update_json_response(cmd, _resp):
    try:
        discuss = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    discuss_form = discuss_facade.discuss_form()
    return JsonResponse(discuss_form.fill_with_model(discuss))

