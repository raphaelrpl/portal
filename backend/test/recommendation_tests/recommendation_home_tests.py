# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from recommendation_app.model import Recommendation
from routes.recommendations.home import index, delete
from gaebusiness.business import CommandExecutionException
from gaegraph.model import Node
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Recommendation)
        template_response = index()
        self.assert_can_render(template_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        recommendation = mommy.save_one(Recommendation)
        redirect_response = delete(recommendation.key.id())
        self.assertIsInstance(redirect_response, RedirectResponse)
        self.assertIsNone(recommendation.key.get())

    def test_non_recommendation_deletion(self):
        non_recommendation = mommy.save_one(Node)
        self.assertRaises(CommandExecutionException, delete, non_recommendation.key.id())
        self.assertIsNotNone(non_recommendation.key.get())

