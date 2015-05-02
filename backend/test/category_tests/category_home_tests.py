# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from category_app.category_model import Category
from routes.categorys.home import index, delete
from gaebusiness.business import CommandExecutionException
from gaegraph.model import Node
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Category)
        template_response = index()
        self.assert_can_render(template_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        category = mommy.save_one(Category)
        redirect_response = delete(category.key.id())
        self.assertIsInstance(redirect_response, RedirectResponse)
        self.assertIsNone(category.key.get())

    def test_non_category_deletion(self):
        non_category = mommy.save_one(Node)
        self.assertRaises(CommandExecutionException, delete, non_category.key.id())
        self.assertIsNotNone(non_category.key.get())

