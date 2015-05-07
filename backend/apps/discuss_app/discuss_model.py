# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from base_app.model import BasePost
from badge_app.badge_model import UserBase, Badge
from gaegraph.model import Arc
from question_app.question_model import Question
from category_app.category_model import Category


class Discuss(BasePost):
    title = ndb.StringProperty(required=True)
    content = ndb.StringProperty(required=True)
    image = ndb.TextProperty(required=False)

    @classmethod
    def count_discusses_by_user(cls, user):
        return cls.query(Discuss.user == user).count()

    @classmethod
    def has_badge_done(cls, user):
        return UserBase.query(UserBase.origin == user)

    def _post_put_hook(self, future):
        discusses = self.count_discusses_by_user(self.user)
        questions = Question.count_questions_by_user(self.user)
        badges = Badge.query().fetch()
        for badge in badges:
            if discusses >= badge.discuss_qt and questions >= badge.question_qt:
                # insert badge
                b = UserBase(origin=self.user, destination=badge)
                # b.put()
                pass

        super(Discuss, self)._post_put_hook(future)


class CategoryDiscuss(Arc):
    origin = ndb.KeyProperty(Category, required=True)
    destination = ndb.KeyProperty(Discuss, required=True)
