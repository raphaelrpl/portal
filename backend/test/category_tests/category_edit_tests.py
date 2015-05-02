# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from category_app.category_model import Category
from routes.categorys.edit import index, save
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        category = mommy.save_one(Category)
        template_response = index(category.key.id())
        self.assert_can_render(template_response)


class EditTests(GAETestCase):
    def test_success(self):
        category = mommy.save_one(Category)
        old_properties = category.to_dict()
        redirect_response = save(category.key.id(), name='name_string', slug='slug_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        edited_category = category.key.get()
        self.assertEquals('name_string', edited_category.name)
        self.assertEquals('slug_string', edited_category.slug)
        self.assertNotEqual(old_properties, edited_category.to_dict())

    def test_error(self):
        category = mommy.save_one(Category)
        old_properties = category.to_dict()
        template_response = save(category.key.id())
        errors = template_response.context['errors']
        self.assertSetEqual(set(['name', 'slug']), set(errors.keys()))
        self.assertEqual(old_properties, category.key.get().to_dict())
        self.assert_can_render(template_response)
