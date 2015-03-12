# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node, Arc
from gaepermission.model import MainUser
from google.appengine.api import images


class Avatar(MainUser):
    avatar = ndb.BlobProperty(required=False)

    def before_put(self):
        if self.avatar is not None:
            self.avatar = images.resize(self.avatar, 128, 128)

    def put(self, **kwargs):
        self.before_put()
        super(Avatar, self).put(kwargs)


class BasePost(Node):
    user = ndb.KeyProperty(MainUser, required=True)
    updated_at = ndb.DateTimeProperty(auto_now_add=True)
    recommend = ndb.IntegerProperty()


class Question(BasePost):
    title = ndb.StringProperty(required=True)


# class UserQuestionArc(Arc):
#     origin = ndb.KeyProperty(User)
#     destination = ndb.KeyProperty(Question)


class Discuss(BasePost):
    title = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)


# class UserDiscussArc(Arc):
#     origin = ndb.KeyProperty(User)
#     destination = ndb.KeyProperty(Discuss)


class Comment(BasePost):
    message = ndb.StringProperty(required=True)