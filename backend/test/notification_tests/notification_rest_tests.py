# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, date
from decimal import Decimal
from base import GAETestCase
from notification_app.notification_model import Notification
from routes.notifications import rest
from gaegraph.model import Node
from mock import Mock
from mommygae import mommy


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Notification)
        mommy.save_one(Notification)
        json_response = rest.index()
        context = json_response.context
        self.assertEqual(2, len(context))
        notification_dct = context[0]
        self.assertSetEqual(set(['id', 'creation', 'message']), set(notification_dct.iterkeys()))
        self.assert_can_serialize_as_json(json_response)


class NewTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Notification.query().get())
        json_response = rest.new(None, message='message_string')
        db_notification = Notification.query().get()
        self.assertIsNotNone(db_notification)
        self.assertEquals('message_string', db_notification.message)
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        resp = Mock()
        json_response = rest.new(resp)
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['message']), set(errors.keys()))
        self.assert_can_serialize_as_json(json_response)


class EditTests(GAETestCase):
    def test_success(self):
        notification = mommy.save_one(Notification)
        old_properties = notification.to_dict()
        json_response = rest.edit(None, notification.key.id(), message='message_string')
        db_notification = notification.key.get()
        self.assertEquals('message_string', db_notification.message)
        self.assertNotEqual(old_properties, db_notification.to_dict())
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        notification = mommy.save_one(Notification)
        old_properties = notification.to_dict()
        resp = Mock()
        json_response = rest.edit(resp, notification.key.id())
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['message']), set(errors.keys()))
        self.assertEqual(old_properties, notification.key.get().to_dict())
        self.assert_can_serialize_as_json(json_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        notification = mommy.save_one(Notification)
        rest.delete(None, notification.key.id())
        self.assertIsNone(notification.key.get())

    def test_non_notification_deletion(self):
        non_notification = mommy.save_one(Node)
        response = Mock()
        json_response = rest.delete(response, non_notification.key.id())
        self.assertIsNotNone(non_notification.key.get())
        self.assertEqual(500, response.status_code)
        self.assert_can_serialize_as_json(json_response)

