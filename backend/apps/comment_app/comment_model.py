# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaepermission.model import MainUser
from base_app.model import BasePost, Base


class Comment(Base):
    post = ndb.KeyProperty(BasePost, required=True)
    user = ndb.KeyProperty(MainUser, required=True)
    content = ndb.StringProperty(required=True)

    @classmethod
    def filter_by_question_key(cls, question_id):
        return cls.query(Comment.post == question_id)

    def _post_put_hook(self, future):
        # Save notification
        super(Comment, self)._post_put_hook(future)


class ReplyComment(Base):
    comment = ndb.KeyProperty(Comment, required=True)
    user = ndb.KeyProperty(MainUser, required=True)
    content = ndb.StringProperty(required=True)