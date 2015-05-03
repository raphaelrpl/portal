# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from recommendation_app.model import Recommendation
from routes.recommendations.edit import index, save
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        recommendation = mommy.save_one(Recommendation)
        template_response = index(recommendation.key.id())
        self.assert_can_render(template_response)


class EditTests(GAETestCase):
    def test_success(self):
        recommendation = mommy.save_one(Recommendation)
        old_properties = recommendation.to_dict()
        redirect_response = save(recommendation.key.id(), name='name_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        edited_recommendation = recommendation.key.get()
        self.assertEquals('name_string', edited_recommendation.name)
        self.assertNotEqual(old_properties, edited_recommendation.to_dict())

    def test_error(self):
        recommendation = mommy.save_one(Recommendation)
        old_properties = recommendation.to_dict()
        template_response = save(recommendation.key.id())
        errors = template_response.context['errors']
        self.assertSetEqual(set(['name']), set(errors.keys()))
        self.assertEqual(old_properties, recommendation.key.get().to_dict())
        self.assert_can_render(template_response)
