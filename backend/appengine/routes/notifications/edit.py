# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from notification_app import notification_facade
from routes import notifications
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index(notification_id):
    notification = notification_facade.get_notification_cmd(notification_id)()
    notification_form = notification_facade.notification_form()
    context = {'save_path': router.to_path(save, notification_id), 'notification': notification_form.fill_with_model(notification)}
    return TemplateResponse(context, 'notifications/notification_form.html')


def save(notification_id, **notification_properties):
    cmd = notification_facade.update_notification_cmd(notification_id, **notification_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors, 'notification': notification_properties}

        return TemplateResponse(context, 'notifications/notification_form.html')
    return RedirectResponse(router.to_path(notifications))

