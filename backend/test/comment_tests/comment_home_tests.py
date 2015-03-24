# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from comment_app.comment_model import Comment
from routes.comments.home import index, delete
from gaebusiness.business import CommandExecutionException
from gaegraph.model import Node
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Comment)
        template_response = index()
        self.assert_can_render(template_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        comment = mommy.save_one(Comment)
        redirect_response = delete(comment.key.id())
        self.assertIsInstance(redirect_response, RedirectResponse)
        self.assertIsNone(comment.key.get())

    def test_non_comment_deletion(self):
        non_comment = mommy.save_one(Node)
        self.assertRaises(CommandExecutionException, delete, non_comment.key.id())
        self.assertIsNotNone(non_comment.key.get())

