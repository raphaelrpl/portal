# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from badge_app.badge_model import Badge
from routes.badges.edit import index, save
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        badge = mommy.save_one(Badge)
        template_response = index(badge.key.id())
        self.assert_can_render(template_response)


class EditTests(GAETestCase):
    def test_success(self):
        badge = mommy.save_one(Badge)
        old_properties = badge.to_dict()
        redirect_response = save(badge.key.id(), name='name_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        edited_badge = badge.key.get()
        self.assertEquals('name_string', edited_badge.name)
        self.assertNotEqual(old_properties, edited_badge.to_dict())

    def test_error(self):
        badge = mommy.save_one(Badge)
        old_properties = badge.to_dict()
        template_response = save(badge.key.id())
        errors = template_response.context['errors']
        self.assertSetEqual(set(['name']), set(errors.keys()))
        self.assertEqual(old_properties, badge.key.get().to_dict())
        self.assert_can_render(template_response)
