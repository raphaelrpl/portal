# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from permission_app.permission_facade import main_user_form
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required
from gaepermission.model import MainUser
from profile_app.profile_model import Profile
from profile_app.profile_facade import profile_form


@login_required
@no_csrf
def index(user_id):
    if user_id:
        return TemplateResponse(template_path="users/user.html")
    pform = profile_form()
    uform = main_user_form()

    def localized_data(model, form):
        model_dct = form.fill_with_model(model)
        profile = Profile.query(Profile.user == model.key).fetch()
        if profile:
            profile = profile[0]
            model_dct['profile'] = pform.fill_with_model(profile)
        else:
            model_dct['profile'] = {}
        return model_dct

    users = MainUser.query().fetch()

    users_output = [localized_data(u, uform) for u in users]

    return TemplateResponse()