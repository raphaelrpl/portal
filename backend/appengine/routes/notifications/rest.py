# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required
from permission_app.permission_facade import main_user_form
from tekton.gae.middleware.json_middleware import JsonResponse
from notification_app import notification_facade
from datetime import datetime
from gaepermission.model import MainUser
from notification_app.notification_model import Notification


def get_the_user(model, facade_form):
    model_dct = facade_form.fill_with_model(model)
    user_form = main_user_form()
    model_dct['sender'] = user_form.fill_with_model(MainUser.get_by_id(int(model.sender.id())))
    model_dct['user'] = user_form.fill_with_model(MainUser.get_by_id(int(model.user.id())))
    model.created_at = datetime.now() - model.creation
    return model_dct


@login_required
@no_csrf
def index(_logged_user):
    # cmd = notification_facade.list_notifications_cmd()
    notifications = Notification.query(Notification.user == _logged_user.key).fetch()
    # notification_list = cmd()
    notification_form = notification_facade.notification_form()
    # notification_dcts = [notification_form.fill_with_model(m) for m in notification_list]
    notification_dcts = [get_the_user(m, notification_form) for m in notifications]
    return JsonResponse(notification_dcts)


@login_required
def new(_resp, **notification_properties):
    cmd = notification_facade.save_notification_cmd(**notification_properties)
    return _save_or_update_json_response(cmd, _resp)


@login_required
def edit(_resp, id, **notification_properties):
    cmd = notification_facade.update_notification_cmd(id, **notification_properties)
    return _save_or_update_json_response(cmd, _resp)


@login_required
def delete(_resp, id):
    cmd = notification_facade.delete_notification_cmd(id)
    try:
        cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)


def _save_or_update_json_response(cmd, _resp):
    try:
        notification = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    notification_form = notification_facade.notification_form()
    return JsonResponse(notification_form.fill_with_model(notification))

