# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaepermission.model import MainUser
from base_app.model import BasePost, Base


class Comment(Base):
    # post = ndb.KeyProperty(BasePost, required=True)
    user = ndb.KeyProperty(MainUser, required=True)
    content = ndb.StringProperty(required=True)