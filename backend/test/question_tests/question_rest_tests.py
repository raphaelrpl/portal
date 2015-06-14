# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import TestQuestion
from question_app.question_model import Question
from routes.questions import rest
from gaegraph.model import Node
from mock import Mock
from mommygae import mommy


class IndexTests(TestQuestion):
    def test_success(self):
        user = self.get_and_insert_dummy_user()
        self.insert_dummy_question("Question 1", user=user)
        self.insert_dummy_question("Question 2", user=user)
        json_response = rest.index()
        context = json_response.context
        self.assertEqual(2, len(context))
        question_dct = context[0]
        self.assertSetEqual(set(['id', 'creation', 'name', 'user', 'updated_at']), set(question_dct.iterkeys()))
        self.assertEqual("Question 1", question_dct['name'])
        self.assert_can_serialize_as_json(json_response)


class NewTests(TestQuestion):
    def test_success(self):
        self.assertIsNone(Question.query().get())
        # json_response = rest.new(_resp=resp, _logged_user=self.get_and_insert_dummy_user(), name='name_string')
        json_response = self.insert_dummy_question("My Question")
        db_question = Question.query().get()
        user = db_question.user.get()
        self.assertIsNotNone(db_question)
        self.assertEquals('My Question', db_question.name)
        self.assertEquals('user@user.com', user.email)
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        resp = Mock()
        user = self.get_and_insert_dummy_user()
        json_response = rest.new(resp, _logged_user=user, **{})
        errors = json_response.context
        self.assertEqual(400, resp.status_code)
        self.assertSetEqual(set(['name']), set(errors.keys()))
        self.assert_can_serialize_as_json(json_response)


class EditTests(TestQuestion):
    def test_success(self):
        # question = mommy.save_one(Question)
        user = self.get_and_insert_dummy_user()
        old_properties = self.insert_dummy_question(name="Question Version 1", user=user).context
        # old_properties = question.to_dict()
        resp = Mock()
        new_properties = dict(old_properties)
        new_properties['user'] = {'id': user.key.id()}
        new_properties['name'] = 'Question Version 2'
        json_response = rest.edit(_resp=resp, _logged_user=user, **new_properties)
        db_question = self.get_question_by_id(old_properties['id'])
        self.assertEquals('Question Version 2', db_question.name)
        self.assertNotEqual(old_properties, db_question.to_dict())
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        # question = mommy.save_one(Question)
        user = self.get_and_insert_dummy_user()

        # Insert dummy question
        self.insert_dummy_question(name="Question Version 1", user=user)

        question = Question.query().get()
        from question_app.question_facade import question_form

        form = question_form()
        old_properties = form.fill_with_model(question)
        dct = dict(old_properties)
        # Set invalid User ID
        dct['user'] = {'id': "20981"}
        resp = Mock()
        json_response = rest.edit(_resp=resp, _logged_user=user, **dct)
        errors = json_response.context
        # question = self.get_question_by_id(old_properties['id'])
        self.assertEqual(400, resp.status_code)
        self.assertSetEqual(set(['name']), set(errors.keys()))
        self.assertEqual(old_properties['name'], question.key.get().name)
        self.assert_can_serialize_as_json(json_response)


class DeleteTests(TestQuestion):
    def test_success(self):
        resp = Mock()
        self.insert_dummy_question("This Question Will Be Deleted")
        question = Question.query().get()
        rest.delete(_resp=resp, id=question.key.id())
        self.assertIsNone(question.key.get())

    def test_non_question_deletion(self):
        non_question = mommy.save_one(Node)
        response = Mock()
        json_response = rest.delete(response, non_question.key.id())
        self.assertIsNotNone(non_question.key.get())
        self.assertEqual(500, response.status_code)
        self.assert_can_serialize_as_json(json_response)

