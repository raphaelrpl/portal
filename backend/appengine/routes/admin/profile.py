# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from config.template_middleware import TemplateResponse
from gaepermission.decorator import login_required
from permission_app.permission_facade import main_user_form
from json import dumps
from profile_app.profile_model import Profile
from profile_app.profile_facade import profile_form
from tekton import router
from routes.profiles.rest import new
from notification_app.notification_model import Notification
from notification_app.notification_facade import notification_form
from gaepermission.model import MainUser


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
    notifications = Notification.query(Notification.sender == _logged_user.key).fetch()

    nform = notification_form()

    def get_the_user(model, facade_form):
        model_dct = facade_form.fill_with_model(model)
        model_dct['sender'] = form.fill_with_model(MainUser.get_by_id(int(model.sender.id())))
        model_dct['user'] = form.fill_with_model(MainUser.get_by_id(int(model.user.id())))
        return model_dct
    notification_dict = [get_the_user(n, nform) for n in notifications]

    context = {"profile": dumps(output),
               "user": dumps(output['user']),
               "new_profile_path": router.to_path(new),
               "activities": dumps(notification_dict)}
    return TemplateResponse(context=context)
