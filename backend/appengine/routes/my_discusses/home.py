# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from tekton import router
from my_discusses_app.model import Discuss
from datetime import datetime


@no_csrf
def index(discuss=""):
    context = {"discusses_page": router.to_path(index)}
    if discuss:
        query = Discuss.query().fetch()
        context['discuss'] = query
        return TemplateResponse(template_path="discusses/discuss.html", context=context)
    # query = Discuss.query().order(Discuss.creation).fetch()[:10][::-1]
    query = [
        {
            "key": 54323122,
            "title": "Lorem Ipsum San Shi",
            "content": "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam",
            "creation": datetime.now() - datetime.now(),
            "image": "/static/img/python.jpg"
        },
        {
            "key": 54323154,
            "title": "Lorem Ipsum San Shi",
            "content": "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam",
            "creation": datetime.now() - datetime.now(),
            "image": "/static/img/python.jpg"
        }
    ]
    context['discusses'] = query
    return TemplateResponse(context)