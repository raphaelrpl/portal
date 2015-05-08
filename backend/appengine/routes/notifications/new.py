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
def index():
    return TemplateResponse({'save_path': router.to_path(save)}, 'notifications/notification_form.html')


def save(**notification_properties):
    cmd = notification_facade.save_notification_cmd(**notification_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'notification': notification_properties}

        return TemplateResponse(context, 'notifications/notification_form.html')
    return RedirectResponse(router.to_path(notifications))

