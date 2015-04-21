# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, date
from decimal import Decimal
from base import GAETestCase
from badge_app.badge_model import Badge
from routes.badges import rest
from gaegraph.model import Node
from mock import Mock
from mommygae import mommy


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Badge)
        mommy.save_one(Badge)
        json_response = rest.index()
        context = json_response.context
        self.assertEqual(2, len(context))
        badge_dct = context[0]
        self.assertSetEqual(set(['id', 'creation', 'name']), set(badge_dct.iterkeys()))
        self.assert_can_serialize_as_json(json_response)


class NewTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Badge.query().get())
        json_response = rest.new(None, name='name_string')
        db_badge = Badge.query().get()
        self.assertIsNotNone(db_badge)
        self.assertEquals('name_string', db_badge.name)
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        resp = Mock()
        json_response = rest.new(resp)
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['name']), set(errors.keys()))
        self.assert_can_serialize_as_json(json_response)


class EditTests(GAETestCase):
    def test_success(self):
        badge = mommy.save_one(Badge)
        old_properties = badge.to_dict()
        json_response = rest.edit(None, badge.key.id(), name='name_string')
        db_badge = badge.key.get()
        self.assertEquals('name_string', db_badge.name)
        self.assertNotEqual(old_properties, db_badge.to_dict())
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        badge = mommy.save_one(Badge)
        old_properties = badge.to_dict()
        resp = Mock()
        json_response = rest.edit(resp, badge.key.id())
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['name']), set(errors.keys()))
        self.assertEqual(old_properties, badge.key.get().to_dict())
        self.assert_can_serialize_as_json(json_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        badge = mommy.save_one(Badge)
        rest.delete(None, badge.key.id())
        self.assertIsNone(badge.key.get())

    def test_non_badge_deletion(self):
        non_badge = mommy.save_one(Node)
        response = Mock()
        json_response = rest.delete(response, non_badge.key.id())
        self.assertIsNotNone(non_badge.key.get())
        self.assertEqual(500, response.status_code)
        self.assert_can_serialize_as_json(json_response)

