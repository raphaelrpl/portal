# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from profile_app.profile_model import Profile
from routes.profiles.new import index, save
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        template_response = index()
        self.assert_can_render(template_response)


class SaveTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Profile.query().get())
        redirect_response = save(position='position_string', about='about_string', education='education_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        saved_profile = Profile.query().get()
        self.assertIsNotNone(saved_profile)
        self.assertEquals('position_string', saved_profile.position)
        self.assertEquals('about_string', saved_profile.about)
        self.assertEquals('education_string', saved_profile.education)

    def test_error(self):
        template_response = save()
        errors = template_response.context['errors']
        self.assertSetEqual(set(['position', 'about', 'education']), set(errors.keys()))
        self.assert_can_render(template_response)
