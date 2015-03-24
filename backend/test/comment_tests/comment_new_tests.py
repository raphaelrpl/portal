# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from comment_app.comment_model import Comment
from routes.comments.new import index, save
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        template_response = index()
        self.assert_can_render(template_response)


class SaveTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Comment.query().get())
        redirect_response = save(content='content_string', updated_at='1/1/2014 01:2:0')
        self.assertIsInstance(redirect_response, RedirectResponse)
        saved_comment = Comment.query().get()
        self.assertIsNotNone(saved_comment)
        self.assertEquals('content_string', saved_comment.content)
        self.assertEquals(datetime(2014, 1, 1, 1, 2, 0), saved_comment.updated_at)

    def test_error(self):
        template_response = save()
        errors = template_response.context['errors']
        self.assertSetEqual(set(['content', 'updated_at']), set(errors.keys()))
        self.assert_can_render(template_response)
