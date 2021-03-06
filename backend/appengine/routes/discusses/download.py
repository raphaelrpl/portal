# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required


@login_required
@no_csrf
def index(_handler, blob_key):
    _handler.send_blob(blob_key)