# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from notification_app.notification_model import Notification
from routes.notifications.edit import index, save
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        notification = mommy.save_one(Notification)
        template_response = index(notification.key.id())
        self.assert_can_render(template_response)


class EditTests(GAETestCase):
    def test_success(self):
        notification = mommy.save_one(Notification)
        old_properties = notification.to_dict()
        redirect_response = save(notification.key.id(), message='message_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        edited_notification = notification.key.get()
        self.assertEquals('message_string', edited_notification.message)
        self.assertNotEqual(old_properties, edited_notification.to_dict())

    def test_error(self):
        notification = mommy.save_one(Notification)
        old_properties = notification.to_dict()
        template_response = save(notification.key.id())
        errors = template_response.context['errors']
        self.assertSetEqual(set(['message']), set(errors.keys()))
        self.assertEqual(old_properties, notification.key.get().to_dict())
        self.assert_can_render(template_response)
