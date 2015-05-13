# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from notification_app.notification_model import Notification
from routes.notifications.home import index, delete
from gaebusiness.business import CommandExecutionException
from gaegraph.model import Node
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Notification)
        template_response = index()
        self.assert_can_render(template_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        notification = mommy.save_one(Notification)
        redirect_response = delete(notification.key.id())
        self.assertIsInstance(redirect_response, RedirectResponse)
        self.assertIsNone(notification.key.get())

    def test_non_notification_deletion(self):
        non_notification = mommy.save_one(Node)
        self.assertRaises(CommandExecutionException, delete, non_notification.key.id())
        self.assertIsNotNone(non_notification.key.get())

