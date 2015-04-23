# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Arc
from gaepermission.model import MainUser
from base_app.model import Base


class Restriction(Base):
    name = ndb.StringProperty(required=True)
    restriction = ndb.KeyProperty(required=True)


class Badge(Base):
    name = ndb.StringProperty(required=True)
    image = ndb.TextProperty(required=True)
    description = ndb.TextProperty(required=False)
    # user = ndb.KeyProperty(MainUser, required=True)
    question_qt = ndb.IntegerProperty(required=True, default=0)
    discuss_qt = ndb.IntegerProperty(required=True, default=0)


class UserBase(Arc):
    origin = MainUser
    destination = Badge

    @classmethod
    def get_badges_by_user(cls, user):
        return UserBase.query(UserBase.origin == user)

