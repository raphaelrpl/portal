# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, date
from decimal import Decimal
from base import GAETestCase
from category_app.category_model import Category
from routes.categorys import rest
from gaegraph.model import Node
from mock import Mock
from mommygae import mommy


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Category)
        mommy.save_one(Category)
        json_response = rest.index()
        context = json_response.context
        self.assertEqual(2, len(context))
        category_dct = context[0]
        self.assertSetEqual(set(['id', 'creation', 'name', 'slug']), set(category_dct.iterkeys()))
        self.assert_can_serialize_as_json(json_response)


class NewTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Category.query().get())
        json_response = rest.new(None, name='name_string', slug='slug_string')
        db_category = Category.query().get()
        self.assertIsNotNone(db_category)
        self.assertEquals('name_string', db_category.name)
        self.assertEquals('slug_string', db_category.slug)
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        resp = Mock()
        json_response = rest.new(resp)
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['name', 'slug']), set(errors.keys()))
        self.assert_can_serialize_as_json(json_response)


class EditTests(GAETestCase):
    def test_success(self):
        category = mommy.save_one(Category)
        old_properties = category.to_dict()
        json_response = rest.edit(None, category.key.id(), name='name_string', slug='slug_string')
        db_category = category.key.get()
        self.assertEquals('name_string', db_category.name)
        self.assertEquals('slug_string', db_category.slug)
        self.assertNotEqual(old_properties, db_category.to_dict())
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        category = mommy.save_one(Category)
        old_properties = category.to_dict()
        resp = Mock()
        json_response = rest.edit(resp, category.key.id())
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['name', 'slug']), set(errors.keys()))
        self.assertEqual(old_properties, category.key.get().to_dict())
        self.assert_can_serialize_as_json(json_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        category = mommy.save_one(Category)
        rest.delete(None, category.key.id())
        self.assertIsNone(category.key.get())

    def test_non_category_deletion(self):
        non_category = mommy.save_one(Node)
        response = Mock()
        json_response = rest.delete(response, non_category.key.id())
        self.assertIsNotNone(non_category.key.get())
        self.assertEqual(500, response.status_code)
        self.assert_can_serialize_as_json(json_response)

