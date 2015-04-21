# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from badge_app.badge_model import Badge
from routes.badges.home import index, delete
from gaebusiness.business import CommandExecutionException
from gaegraph.model import Node
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Badge)
        template_response = index()
        self.assert_can_render(template_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        badge = mommy.save_one(Badge)
        redirect_response = delete(badge.key.id())
        self.assertIsInstance(redirect_response, RedirectResponse)
        self.assertIsNone(badge.key.get())

    def test_non_badge_deletion(self):
        non_badge = mommy.save_one(Node)
        self.assertRaises(CommandExecutionException, delete, non_badge.key.id())
        self.assertIsNotNone(non_badge.key.get())

