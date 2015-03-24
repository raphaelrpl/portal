# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, date
from decimal import Decimal
from base import GAETestCase
from comment_app.comment_model import Comment
from routes.comments import rest
from gaegraph.model import Node
from mock import Mock
from mommygae import mommy


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Comment)
        mommy.save_one(Comment)
        json_response = rest.index()
        context = json_response.context
        self.assertEqual(2, len(context))
        comment_dct = context[0]
        self.assertSetEqual(set(['id', 'creation', 'content', 'updated_at']), set(comment_dct.iterkeys()))
        self.assert_can_serialize_as_json(json_response)


class NewTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Comment.query().get())
        json_response = rest.new(None, content='content_string', updated_at='1/1/2014 01:2:0')
        db_comment = Comment.query().get()
        self.assertIsNotNone(db_comment)
        self.assertEquals('content_string', db_comment.content)
        self.assertEquals(datetime(2014, 1, 1, 1, 2, 0), db_comment.updated_at)
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        resp = Mock()
        json_response = rest.new(resp)
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['content', 'updated_at']), set(errors.keys()))
        self.assert_can_serialize_as_json(json_response)


class EditTests(GAETestCase):
    def test_success(self):
        comment = mommy.save_one(Comment)
        old_properties = comment.to_dict()
        json_response = rest.edit(None, comment.key.id(), content='content_string', updated_at='1/1/2014 01:2:0')
        db_comment = comment.key.get()
        self.assertEquals('content_string', db_comment.content)
        self.assertEquals(datetime(2014, 1, 1, 1, 2, 0), db_comment.updated_at)
        self.assertNotEqual(old_properties, db_comment.to_dict())
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        comment = mommy.save_one(Comment)
        old_properties = comment.to_dict()
        resp = Mock()
        json_response = rest.edit(resp, comment.key.id())
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['content', 'updated_at']), set(errors.keys()))
        self.assertEqual(old_properties, comment.key.get().to_dict())
        self.assert_can_serialize_as_json(json_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        comment = mommy.save_one(Comment)
        rest.delete(None, comment.key.id())
        self.assertIsNone(comment.key.get())

    def test_non_comment_deletion(self):
        non_comment = mommy.save_one(Node)
        response = Mock()
        json_response = rest.delete(response, non_comment.key.id())
        self.assertIsNotNone(non_comment.key.get())
        self.assertEqual(500, response.status_code)
        self.assert_can_serialize_as_json(json_response)

