# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from routes.login.home import prepare_login_services
from discusses_app.forms import UserForm
from tekton import router
from tekton.gae.middleware.redirect import RedirectResponse


@login_not_required
@no_csrf
def index(ret_path="/"):
    dct = prepare_login_services(ret_path)
    dct["submit_url"] = router.to_path(process)
    return TemplateResponse(dct)


@login_not_required
@no_csrf
def process(**profile):
    form = UserForm(**profile)
    path = router.to_path(index)
    print(profile)
    print path
    return RedirectResponse(path)
