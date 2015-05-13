# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from notification_app.notification_model import Notification
from routes.notifications.new import index, save
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        template_response = index()
        self.assert_can_render(template_response)


class SaveTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Notification.query().get())
        redirect_response = save(message='message_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        saved_notification = Notification.query().get()
        self.assertIsNotNone(saved_notification)
        self.assertEquals('message_string', saved_notification.message)

    def test_error(self):
        template_response = save()
        errors = template_response.context['errors']
        self.assertSetEqual(set(['message']), set(errors.keys()))
        self.assert_can_render(template_response)
