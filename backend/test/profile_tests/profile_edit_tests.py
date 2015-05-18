# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from profile_app.profile_model import Profile
from routes.profiles.edit import index, save
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        profile = mommy.save_one(Profile)
        template_response = index(profile.key.id())
        self.assert_can_render(template_response)


class EditTests(GAETestCase):
    def test_success(self):
        profile = mommy.save_one(Profile)
        old_properties = profile.to_dict()
        redirect_response = save(profile.key.id(), position='position_string', about='about_string', education='education_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        edited_profile = profile.key.get()
        self.assertEquals('position_string', edited_profile.position)
        self.assertEquals('about_string', edited_profile.about)
        self.assertEquals('education_string', edited_profile.education)
        self.assertNotEqual(old_properties, edited_profile.to_dict())

    def test_error(self):
        profile = mommy.save_one(Profile)
        old_properties = profile.to_dict()
        template_response = save(profile.key.id())
        errors = template_response.context['errors']
        self.assertSetEqual(set(['position', 'about', 'education']), set(errors.keys()))
        self.assertEqual(old_properties, profile.key.get().to_dict())
        self.assert_can_render(template_response)
