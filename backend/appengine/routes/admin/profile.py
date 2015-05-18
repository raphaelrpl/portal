# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from config.template_middleware import TemplateResponse
from gaepermission.decorator import login_required
from permission_app.permission_facade import main_user_form
from json import dumps
from profile_app.profile_model import Profile
from profile_app.profile_facade import profile_form


@login_required
@no_csrf
def index(_logged_user):
    form = main_user_form()
    pform = profile_form()
    profile = Profile.query(Profile.user == _logged_user.key).fetch()
    output = {}
    if profile:
        profile = profile[0]
        output = pform.fill_with_model(profile)
    output['user'] = form.fill_with_model(_logged_user)
    context = {"profile": dumps(output),
               "user": dumps(output['user'])}
    return TemplateResponse(context=context)
