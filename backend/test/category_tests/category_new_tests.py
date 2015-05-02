# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from category_app.category_model import Category
from routes.categorys.new import index, save
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        template_response = index()
        self.assert_can_render(template_response)


class SaveTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Category.query().get())
        redirect_response = save(name='name_string', slug='slug_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        saved_category = Category.query().get()
        self.assertIsNotNone(saved_category)
        self.assertEquals('name_string', saved_category.name)
        self.assertEquals('slug_string', saved_category.slug)

    def test_error(self):
        template_response = save()
        errors = template_response.context['errors']
        self.assertSetEqual(set(['name', 'slug']), set(errors.keys()))
        self.assert_can_render(template_response)
