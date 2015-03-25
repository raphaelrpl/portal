# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from config.template_middleware import TemplateResponse
from datetime import datetime
from gaepermission.decorator import login_not_required
from tekton import router


@login_not_required
@no_csrf
def index(message_id=""):
    if message_id:
        context = {
            "message": {
                "key": "1235721",
                "sender": "Fulano",
                "content": "Lorem isu dore",
                "creation": datetime.now()
            }
        }
        return TemplateResponse(context=context, template_path="admin/messages/message.html")
    context = {
        "messages_path": router.to_path(index),
        "messages": [
            {
                "key": "1235721",
                "sender": "Fulano",
                "content": "Lorem isu dore",
                "creation": datetime.now()
            },
            {
                "key": "1233436",
                "sender": "Fulano",
                "content": "Lorem isu dore",
                "creation": datetime.now()
            },
            {
                "key": "1237549",
                "sender": "Fulano",
                "content": "Lorem isu dore",
                "creation": datetime.now()
            }
        ]
    }
    return TemplateResponse(context=context)
