# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required
from tekton.gae.middleware.json_middleware import JsonResponse
from profile_app import profile_facade


@login_required
def index():
    cmd = profile_facade.list_profiles_cmd()
    profile_list = cmd()
    profile_form = profile_facade.profile_form()
    profile_dcts = [profile_form.fill_with_model(m) for m in profile_list]
    return JsonResponse(profile_dcts)


@login_required
def new(_resp, _logged_user, **profile_properties):
    identifier = profile_properties.get('id')
    if identifier:
        # Edit
        cmd = profile_facade.update_profile_cmd(identifier, **profile_properties)
    else:
        # New
        cmd = profile_facade.save_profile_cmd(**profile_properties)
    return _save_or_update_json_response(cmd, _resp, _logged_user)


@login_required
def edit(_resp, _logged_user, id, **profile_properties):
    cmd = profile_facade.update_profile_cmd(id, **profile_properties)
    return _save_or_update_json_response(cmd, _resp, _logged_user)


@login_required
def delete(_resp, id):
    cmd = profile_facade.delete_profile_cmd(id)
    try:
        cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)


def _save_or_update_json_response(cmd, _resp, _logged_user):
    cmd.form.user = _logged_user
    try:
        profile = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    profile_form = profile_facade.profile_form()
    return JsonResponse(profile_form.fill_with_model(profile))

