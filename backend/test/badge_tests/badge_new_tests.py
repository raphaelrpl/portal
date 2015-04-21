# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from badge_app.badge_model import Badge
from routes.badges.new import index, save
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        template_response = index()
        self.assert_can_render(template_response)


class SaveTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Badge.query().get())
        redirect_response = save(name='name_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        saved_badge = Badge.query().get()
        self.assertIsNotNone(saved_badge)
        self.assertEquals('name_string', saved_badge.name)

    def test_error(self):
        template_response = save()
        errors = template_response.context['errors']
        self.assertSetEqual(set(['name']), set(errors.keys()))
        self.assert_can_render(template_response)
