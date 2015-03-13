# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node
from gaepermission.model import MainUser


class Question(Node):
    user = ndb.KeyProperty(MainUser, required=True)
    updated_at = ndb.DateTimeProperty(auto_now_add=True)
    name = ndb.StringProperty(required=True)

