# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, date
from decimal import Decimal
from base import GAETestCase
from recommendation_app.model import Recommendation
from routes.recommendations import rest
from gaegraph.model import Node
from mock import Mock
from mommygae import mommy


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Recommendation)
        mommy.save_one(Recommendation)
        json_response = rest.index()
        context = json_response.context
        self.assertEqual(2, len(context))
        recommendation_dct = context[0]
        self.assertSetEqual(set(['id', 'creation', 'name']), set(recommendation_dct.iterkeys()))
        self.assert_can_serialize_as_json(json_response)


class NewTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Recommendation.query().get())
        json_response = rest.new(None, name='name_string')
        db_recommendation = Recommendation.query().get()
        self.assertIsNotNone(db_recommendation)
        self.assertEquals('name_string', db_recommendation.name)
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
        recommendation = mommy.save_one(Recommendation)
        old_properties = recommendation.to_dict()
        json_response = rest.edit(None, recommendation.key.id(), name='name_string')
        db_recommendation = recommendation.key.get()
        self.assertEquals('name_string', db_recommendation.name)
        self.assertNotEqual(old_properties, db_recommendation.to_dict())
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        recommendation = mommy.save_one(Recommendation)
        old_properties = recommendation.to_dict()
        resp = Mock()
        json_response = rest.edit(resp, recommendation.key.id())
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['name']), set(errors.keys()))
        self.assertEqual(old_properties, recommendation.key.get().to_dict())
        self.assert_can_serialize_as_json(json_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        recommendation = mommy.save_one(Recommendation)
        rest.delete(None, recommendation.key.id())
        self.assertIsNone(recommendation.key.get())

    def test_non_recommendation_deletion(self):
        non_recommendation = mommy.save_one(Node)
        response = Mock()
        json_response = rest.delete(response, non_recommendation.key.id())
        self.assertIsNotNone(non_recommendation.key.get())
        self.assertEqual(500, response.status_code)
        self.assert_can_serialize_as_json(json_response)

