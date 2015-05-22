# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from base_app.model import BasePost
from gaegraph.model import Arc
from category_app.category_model import Category
from notification_app.notification_model import Notification


class Question(BasePost):
    name = ndb.StringProperty(required=True)

    @classmethod
    def count_questions_by_user(cls, user):
        return cls.query(Question.user == user).count()

    def _post_put_hook(self, future):
        super(Question, self)._post_put_hook(future)
        post = self
        notification = Notification(sender=self.user, message="publicou uma questão", user=post.user)
        notification.notification_type = "question"
        notification.post = self.key.id()
        notification.put()


class CategoryQuestion(Arc):
    origin = ndb.KeyProperty(Category, required=True)
    destination = ndb.KeyProperty(Question, required=True)