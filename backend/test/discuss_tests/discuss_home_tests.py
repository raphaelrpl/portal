# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from discuss_app.discuss_model import Discuss
from routes.discusses.home import index, delete
from gaebusiness.business import CommandExecutionException
from gaegraph.model import Node
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Discuss)
        template_response = index()
        self.assert_can_render(template_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        discuss = mommy.save_one(Discuss)
        redirect_response = delete(discuss.key.id())
        self.assertIsInstance(redirect_response, RedirectResponse)
        self.assertIsNone(discuss.key.get())

    def test_non_discuss_deletion(self):
        non_discuss = mommy.save_one(Node)
        self.assertRaises(CommandExecutionException, delete, non_discuss.key.id())
        self.assertIsNotNone(non_discuss.key.get())

