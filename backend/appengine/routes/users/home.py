# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf


@no_csrf
def index(user_id):
    if user_id:
        return TemplateResponse(template_path="users/user.html")
    return TemplateResponse()