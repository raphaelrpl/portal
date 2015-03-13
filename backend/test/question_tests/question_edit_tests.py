# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from question_app.question_model import Question
from routes.questions.edit import index, save
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        question = mommy.save_one(Question)
        template_response = index(question.key.id())
        self.assert_can_render(template_response)


class EditTests(GAETestCase):
    def test_success(self):
        question = mommy.save_one(Question)
        old_properties = question.to_dict()
        redirect_response = save(question.key.id(), name='name_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        edited_question = question.key.get()
        self.assertEquals('name_string', edited_question.name)
        self.assertNotEqual(old_properties, edited_question.to_dict())

    def test_error(self):
        question = mommy.save_one(Question)
        old_properties = question.to_dict()
        template_response = save(question.key.id())
        errors = template_response.context['errors']
        self.assertSetEqual(set(['name']), set(errors.keys()))
        self.assertEqual(old_properties, question.key.get().to_dict())
        self.assert_can_render(template_response)
