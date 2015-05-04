# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from tekton.gae.middleware.json_middleware import JsonResponse
from badge_app import badge_facade
from gaepermission.decorator import login_required


@login_required
def index():
    cmd = badge_facade.list_badges_cmd()
    badge_list = cmd()
    badge_form = badge_facade.badge_form()
    badge_dcts = [badge_form.fill_with_model(m) for m in badge_list]
    return JsonResponse(badge_dcts)


@login_required
def new(_resp, **badge_properties):
    cmd = badge_facade.save_badge_cmd(**badge_properties)
    return _save_or_update_json_response(cmd, _resp)


@login_required
def edit(_resp, id, **badge_properties):
    cmd = badge_facade.update_badge_cmd(id, **badge_properties)
    return _save_or_update_json_response(cmd, _resp)


@login_required
def delete(_resp, id):
    cmd = badge_facade.delete_badge_cmd(id)
    try:
        cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)


def _save_or_update_json_response(cmd, _resp):
    try:
        badge = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    badge_form = badge_facade.badge_form()
    return JsonResponse(badge_form.fill_with_model(badge))

