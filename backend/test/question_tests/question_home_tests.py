# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from question_app.question_model import Question
from routes.questions.home import index, delete
from gaebusiness.business import CommandExecutionException
from gaegraph.model import Node
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Question)
        template_response = index()
        self.assert_can_render(template_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        question = mommy.save_one(Question)
        redirect_response = delete(question.key.id())
        self.assertIsInstance(redirect_response, RedirectResponse)
        self.assertIsNone(question.key.get())

    def test_non_question_deletion(self):
        non_question = mommy.save_one(Node)
        self.assertRaises(CommandExecutionException, delete, non_question.key.id())
        self.assertIsNotNone(non_question.key.get())

