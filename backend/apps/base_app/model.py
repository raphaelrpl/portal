# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.model import Node
from google.appengine.ext import ndb
from gaepermission.model import MainUser


class Base(Node):
    updated_at = ndb.DateTimeProperty(auto_now=True)


class BasePost(Base):
    user = ndb.KeyProperty(MainUser, required=True)