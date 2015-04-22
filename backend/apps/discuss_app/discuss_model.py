# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from base_app.model import BasePost


class Discuss(BasePost):
    title = ndb.StringProperty(required=True)
    content = ndb.StringProperty(required=True)
    image = ndb.TextProperty(required=False)

