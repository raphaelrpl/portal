# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from notification_app import notification_facade
from routes.notifications import new, edit
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index():
    cmd = notification_facade.list_notifications_cmd()
    notifications = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    notification_form = notification_facade.notification_form()

    def localize_notification(notification):
        notification_dct = notification_form.fill_with_model(notification)
        notification_dct['edit_path'] = router.to_path(edit_path, notification_dct['id'])
        notification_dct['delete_path'] = router.to_path(delete_path, notification_dct['id'])
        return notification_dct

    localized_notifications = [localize_notification(notification) for notification in notifications]
    context = {'notifications': localized_notifications,
               'new_path': router.to_path(new)}
    return TemplateResponse(context, 'notifications/notification_home.html')


def delete(notification_id):
    notification_facade.delete_notification_cmd(notification_id)()
    return RedirectResponse(router.to_path(index))

