# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from routes.login.home import prepare_login_services
from discuss_app.model import Discuss
from datetime import datetime


@login_not_required
@no_csrf
def index(discuss=""):
    context = {}
    if discuss:
        query = Discuss.query().fetch()
        context['discuss'] = query
        return TemplateResponse(template_path="discuss/discuss.html", context=context)
    # query = Discuss.query().order(Discuss.creation).fetch()[:10][::-1]
    query = [
        {
            "title": "Lorem Ipsum San Shi",
            "content": "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam",
            "creation": datetime.now() - datetime.now(),
            "image": "/static/img/python.jpg"
        },
        {
            "title": "Lorem Ipsum San Shi",
            "content": "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam",
            "creation": datetime.now() - datetime.now(),
            "image": "/static/img/python.jpg"
        }
    ]
    context['discusses'] = query
    return TemplateResponse(context)