# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from gaecookie.decorator import no_csrf
from tekton.gae.middleware.json_middleware import JsonResponse
from category_app import category_facade
from gaepermission.decorator import login_required


@login_required
@no_csrf
def index():
    cmd = category_facade.list_categorys_cmd()
    category_list = cmd()
    category_form = category_facade.category_form()
    category_dcts = [category_form.fill_with_model(m) for m in category_list]
    return JsonResponse(category_dcts, secure_prefix="")


@login_required
def new(_resp, **category_properties):
    cmd = category_facade.save_category_cmd(**category_properties)
    return _save_or_update_json_response(cmd, _resp)


@login_required
def edit(_resp, id, **category_properties):
    cmd = category_facade.update_category_cmd(id, **category_properties)
    return _save_or_update_json_response(cmd, _resp)


@login_required
def delete(_resp, id):
    cmd = category_facade.delete_category_cmd(id)
    try:
        cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)


def _save_or_update_json_response(cmd, _resp):
    try:
        category = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    category_form = category_facade.category_form()
    return JsonResponse(category_form.fill_with_model(category))

