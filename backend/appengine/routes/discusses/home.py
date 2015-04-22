# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from discuss_app import discuss_facade
from tekton.gae.middleware.redirect import RedirectResponse
from datetime import datetime


@no_csrf
def index(discuss=""):
    context = {"discusses_page": router.to_path(index)}
    if discuss:
        cmd = discuss_facade.get_discuss_cmd(discuss)
        query_discuss = cmd()
        context['discuss'] = query_discuss
        return TemplateResponse(template_path="discusses/discuss.html", context=context)
    # query = Discuss.query().order(Discuss.creation).fetch()[:10][::-1]
    cmd = discuss_facade.ListDiscussCommand()
    discusses = cmd()
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
    context['discusses'] = discusses
    return TemplateResponse(context, template_path="discusses/home.html")

    # cmd = discuss_facade.list_discusss_cmd()
    # discusss = cmd()
    # edit_path = router.to_path(edit)
    # delete_path = router.to_path(delete)
    # discuss_form = discuss_facade.discuss_form()
    #
    # def localize_discuss(discuss):
    #     discuss_dct = discuss_form.fill_with_model(discuss)
    #     discuss_dct['edit_path'] = router.to_path(edit_path, discuss_dct['id'])
    #     discuss_dct['delete_path'] = router.to_path(delete_path, discuss_dct['id'])
    #     return discuss_dct
    #
    # localized_discusss = [localize_discuss(discuss) for discuss in discusss]
    # context = {'discusss': localized_discusss,
    #            'new_path': router.to_path(new)}
    # return TemplateResponse(context, 'discusss/discuss_home.html')


def delete(discuss_id):
    discuss_facade.delete_discuss_cmd(discuss_id)()
    return RedirectResponse(router.to_path(index))

