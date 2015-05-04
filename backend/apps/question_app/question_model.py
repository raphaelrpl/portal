# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from base_app.model import BasePost
from gaegraph.model import Arc
from category_app.category_model import Category


class Question(BasePost):
    name = ndb.StringProperty(required=True)

    @classmethod
    def count_questions_by_user(cls, user):
        return cls.query(Question.user == user).count()


class CategoryQuestion(Arc):
    origin = ndb.KeyProperty(Category, required=True)
    destination = ndb.KeyProperty(Question, required=True)