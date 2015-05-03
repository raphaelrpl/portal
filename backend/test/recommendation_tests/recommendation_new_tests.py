# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from recommendation_app.model import Recommendation
from routes.recommendations.new import index, save
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        template_response = index()
        self.assert_can_render(template_response)


class SaveTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Recommendation.query().get())
        redirect_response = save(name='name_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        saved_recommendation = Recommendation.query().get()
        self.assertIsNotNone(saved_recommendation)
        self.assertEquals('name_string', saved_recommendation.name)

    def test_error(self):
        template_response = save()
        errors = template_response.context['errors']
        self.assertSetEqual(set(['name']), set(errors.keys()))
        self.assert_can_render(template_response)
