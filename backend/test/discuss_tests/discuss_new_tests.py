# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from discuss_app.discuss_model import Discuss
from routes.discusses.new import index, save
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        template_response = index()
        self.assert_can_render(template_response)


class SaveTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Discuss.query().get())
        redirect_response = save(content='content_string', title='title_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        saved_discuss = Discuss.query().get()
        self.assertIsNotNone(saved_discuss)
        self.assertEquals('content_string', saved_discuss.content)
        self.assertEquals('title_string', saved_discuss.title)

    def test_error(self):
        template_response = save()
        errors = template_response.context['errors']
        self.assertSetEqual(set(['content', 'title']), set(errors.keys()))
        self.assert_can_render(template_response)
