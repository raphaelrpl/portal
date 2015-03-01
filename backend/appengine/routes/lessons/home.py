# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required, login_required
from routes.login.home import prepare_login_services


@login_not_required
@no_csrf
def index(ret_path="/"):
    dct = prepare_login_services(ret_path)
    return TemplateResponse(dct)