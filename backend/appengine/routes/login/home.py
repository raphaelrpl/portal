# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api import users
from gaecookie.decorator import no_csrf
from gaepermission import facade
from gaepermission.decorator import login_not_required
from tekton import router
from config.template_middleware import TemplateResponse
from routes.login import google, facebook
from routes.login.passwordless import send_email
from settings import FACEBOOK_APP_ID
import os


def prepare_login_services(ret_path="/"):
    g_path = router.to_path(google.index, ret_path=ret_path)
    dct = {'login_google_path': users.create_login_url(g_path),
           'login_passwordless_path': router.to_path(send_email, ret_path=ret_path),
           'login_facebook_path': router.to_path(facebook.index, ret_path=ret_path),
           'faceapp': facade.get_facebook_app_data().execute().result,
           'facebook_app_id': FACEBOOK_APP_ID}
    return dct


@login_not_required
@no_csrf
def index(ret_path='/'):
    return TemplateResponse(prepare_login_services(ret_path))