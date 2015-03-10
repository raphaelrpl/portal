# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.model import Node
from google.appengine.ext import ndb
from gaepermission.model import MainUser
from google.appengine.api import images


class User(MainUser):
    avatar = ndb.BlobProperty()

    def before_put(self):
        if self.avatar is not None:
            self.avatar = images.resize(self.avatar, 128, 128)

    def put(self, **kwargs):
        self.before_put()
        super(User, self).put(kwargs)


class BasePost(Node):
    # user = ndb.
    updated_at = ndb.DateTimeProperty(auto_now_add=True)
    recommend = ndb.IntegerProperty()


class Question(BasePost):
    title = ndb.StringProperty(required=True)


class Discuss(BasePost):
    title = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)


class Comment(BasePost):
    message = ndb.StringProperty(required=True)