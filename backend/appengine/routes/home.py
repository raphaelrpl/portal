# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required, login_required
from routes.login.home import prepare_login_services
from tekton import router


@login_required
@no_csrf
def index(_logged_user, ret_path="/"):
    dct = prepare_login_services(ret_path)
    # dct['_logged_user'] = _logged_user
    return TemplateResponse(dct)

