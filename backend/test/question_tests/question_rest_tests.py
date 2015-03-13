# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, date
from decimal import Decimal
from base import GAETestCase
from question_app.question_model import Question
from routes.questions import rest
from gaegraph.model import Node
from mock import Mock
from mommygae import mommy


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Question)
        mommy.save_one(Question)
        json_response = rest.index()
        context = json_response.context
        self.assertEqual(2, len(context))
        question_dct = context[0]
        self.assertSetEqual(set(['id', 'creation', 'name']), set(question_dct.iterkeys()))
        self.assert_can_serialize_as_json(json_response)


class NewTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Question.query().get())
        json_response = rest.new(None, name='name_string')
        db_question = Question.query().get()
        self.assertIsNotNone(db_question)
        self.assertEquals('name_string', db_question.name)
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
        question = mommy.save_one(Question)
        old_properties = question.to_dict()
        json_response = rest.edit(None, question.key.id(), name='name_string')
        db_question = question.key.get()
        self.assertEquals('name_string', db_question.name)
        self.assertNotEqual(old_properties, db_question.to_dict())
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        question = mommy.save_one(Question)
        old_properties = question.to_dict()
        resp = Mock()
        json_response = rest.edit(resp, question.key.id())
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['name']), set(errors.keys()))
        self.assertEqual(old_properties, question.key.get().to_dict())
        self.assert_can_serialize_as_json(json_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        question = mommy.save_one(Question)
        rest.delete(None, question.key.id())
        self.assertIsNone(question.key.get())

    def test_non_question_deletion(self):
        non_question = mommy.save_one(Node)
        response = Mock()
        json_response = rest.delete(response, non_question.key.id())
        self.assertIsNotNone(non_question.key.get())
        self.assertEqual(500, response.status_code)
        self.assert_can_serialize_as_json(json_response)

