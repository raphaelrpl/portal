# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, date
from decimal import Decimal
from base import GAETestCase
from discuss_app.discuss_model import Discuss
from routes.discusses import rest
from gaegraph.model import Node
from mock import Mock
from mommygae import mommy


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Discuss)
        mommy.save_one(Discuss)
        json_response = rest.index()
        context = json_response.context
        self.assertEqual(2, len(context))
        discuss_dct = context[0]
        self.assertSetEqual(set(['id', 'creation', 'content', 'title']), set(discuss_dct.iterkeys()))
        self.assert_can_serialize_as_json(json_response)


class NewTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Discuss.query().get())
        json_response = rest.new(None, content='content_string', title='title_string')
        db_discuss = Discuss.query().get()
        self.assertIsNotNone(db_discuss)
        self.assertEquals('content_string', db_discuss.content)
        self.assertEquals('title_string', db_discuss.title)
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        resp = Mock()
        json_response = rest.new(resp)
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['content', 'title']), set(errors.keys()))
        self.assert_can_serialize_as_json(json_response)


class EditTests(GAETestCase):
    def test_success(self):
        discuss = mommy.save_one(Discuss)
        old_properties = discuss.to_dict()
        json_response = rest.edit(None, discuss.key.id(), content='content_string', title='title_string')
        db_discuss = discuss.key.get()
        self.assertEquals('content_string', db_discuss.content)
        self.assertEquals('title_string', db_discuss.title)
        self.assertNotEqual(old_properties, db_discuss.to_dict())
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        discuss = mommy.save_one(Discuss)
        old_properties = discuss.to_dict()
        resp = Mock()
        json_response = rest.edit(resp, discuss.key.id())
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['content', 'title']), set(errors.keys()))
        self.assertEqual(old_properties, discuss.key.get().to_dict())
        self.assert_can_serialize_as_json(json_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        discuss = mommy.save_one(Discuss)
        rest.delete(None, discuss.key.id())
        self.assertIsNone(discuss.key.get())

    def test_non_discuss_deletion(self):
        non_discuss = mommy.save_one(Node)
        response = Mock()
        json_response = rest.delete(response, non_discuss.key.id())
        self.assertIsNotNone(non_discuss.key.get())
        self.assertEqual(500, response.status_code)
        self.assert_can_serialize_as_json(json_response)

