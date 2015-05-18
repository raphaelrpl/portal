# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node
from gaepermission.model import MainUser


class Profile(Node):
    user = ndb.KeyProperty(MainUser, required=True)
    avatar = ndb.StringProperty(required=False)
    education = ndb.StringProperty(required=False)
    position = ndb.StringProperty(required=False)
    about = ndb.TextProperty(required=False)

