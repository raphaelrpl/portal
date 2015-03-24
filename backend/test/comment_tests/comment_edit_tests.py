# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from comment_app.comment_model import Comment
from routes.comments.edit import index, save
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        comment = mommy.save_one(Comment)
        template_response = index(comment.key.id())
        self.assert_can_render(template_response)


class EditTests(GAETestCase):
    def test_success(self):
        comment = mommy.save_one(Comment)
        old_properties = comment.to_dict()
        redirect_response = save(comment.key.id(), content='content_string', updated_at='1/1/2014 01:2:0')
        self.assertIsInstance(redirect_response, RedirectResponse)
        edited_comment = comment.key.get()
        self.assertEquals('content_string', edited_comment.content)
        self.assertEquals(datetime(2014, 1, 1, 1, 2, 0), edited_comment.updated_at)
        self.assertNotEqual(old_properties, edited_comment.to_dict())

    def test_error(self):
        comment = mommy.save_one(Comment)
        old_properties = comment.to_dict()
        template_response = save(comment.key.id())
        errors = template_response.context['errors']
        self.assertSetEqual(set(['content', 'updated_at']), set(errors.keys()))
        self.assertEqual(old_properties, comment.key.get().to_dict())
        self.assert_can_render(template_response)
