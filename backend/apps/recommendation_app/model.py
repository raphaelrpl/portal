# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base_app.model import BasePost
from gaegraph.model import Arc, ndb
from gaepermission.model import MainUser


class Recommendation(Arc):
    origin = ndb.KeyProperty(MainUser, required=True)
    destination = ndb.KeyProperty(BasePost, required=True)

    def _post_put_hook(self, future):
        # Send notification to owner
        super(Recommendation, self)._post_put_hook(future)