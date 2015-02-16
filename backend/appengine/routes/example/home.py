# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from config.template_middleware import TemplateResponse


@login_not_required
@no_csrf
def index(_resp, **kwargs):
    return TemplateResponse()
    # path = router.to_path(function)
    # _handler.redirect(path)


@login_not_required
@no_csrf
def function(_resp, _req, nome):
    _resp.write("Example!!!!\tAAA")