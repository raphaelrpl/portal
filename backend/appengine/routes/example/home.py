# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton import router


@login_not_required
@no_csrf
def index(_resp, **kwargs):
    _resp.write("Example!!!!\tAAA")
    # path = router.to_path(function)
    # _handler.redirect(path)


@login_not_required
@no_csrf
def function(_resp, _req, nome):
    _resp.write("Example!!!!\tAAA")