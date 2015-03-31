# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from discuss_app.discuss_model import Discuss
from routes.discusses.edit import index, save
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        discuss = mommy.save_one(Discuss)
        template_response = index(discuss.key.id())
        self.assert_can_render(template_response)


class EditTests(GAETestCase):
    def test_success(self):
        discuss = mommy.save_one(Discuss)
        old_properties = discuss.to_dict()
        redirect_response = save(discuss.key.id(), content='content_string', title='title_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        edited_discuss = discuss.key.get()
        self.assertEquals('content_string', edited_discuss.content)
        self.assertEquals('title_string', edited_discuss.title)
        self.assertNotEqual(old_properties, edited_discuss.to_dict())

    def test_error(self):
        discuss = mommy.save_one(Discuss)
        old_properties = discuss.to_dict()
        template_response = save(discuss.key.id())
        errors = template_response.context['errors']
        self.assertSetEqual(set(['content', 'title']), set(errors.keys()))
        self.assertEqual(old_properties, discuss.key.get().to_dict())
        self.assert_can_render(template_response)
