# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node
from gaepermission.model import MainUser


class Notification(Node):
    sender = ndb.KeyProperty(MainUser, required=True)
    user = ndb.KeyProperty(MainUser, required=True)
    message = ndb.StringProperty(required=True)
    notification_type = ndb.StringProperty(required=True)
    is_read = ndb.BooleanProperty(required=True, default=False)
