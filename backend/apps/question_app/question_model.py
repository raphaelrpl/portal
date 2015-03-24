# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from base_app.model import BasePost


class Question(BasePost):
    name = ndb.StringProperty(required=True)

