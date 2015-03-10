# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required, login_required
from datetime import datetime
from discuss_app.utils import FriendlyDatetime


@login_not_required
@no_csrf
def index(_logged_user, ret_path="/"):
    formatter = FriendlyDatetime()
    context = {"discusses": [
        {
            "title": "Quais os principais assuntos no tutorship portal?",
            "content": "",
            "image": "/static/img/python.jpg",
            "creation": formatter(datetime(day=10, month=3, year=2015, hour=8))
        },
        {
            "title": "Quais os principais assuntos no tutorship portal?",
            "content": "",
            "image": "/static/img/test.jpg",
            "creation": formatter(datetime(day=9, month=3, year=2015, hour=8))
        }
    ]}
    return TemplateResponse(context=context)

