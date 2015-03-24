# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node
from gaepermission.model import MainUser


class Comment(Node):
    user = ndb.KeyProperty(MainUser, required=True)
    content = ndb.StringProperty(required=True)
    updated_at = ndb.DateTimeProperty(required=True)

