# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Arc
from gaepermission.model import MainUser
from base_app.model import Base


class Badge(Base):
    name = ndb.StringProperty(required=True)
    user = ndb.KeyProperty(MainUser, required=True)
    restriction = ndb.StringProperty(required=True)


class UserBase(Arc):
    origin = MainUser
    destination = Badge

