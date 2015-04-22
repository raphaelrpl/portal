# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaepermission.model import MainUser
from permission_app.permission_facade import main_user_form
from tekton import router
from gaecookie.decorator import no_csrf
from discuss_app import discuss_facade
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index(discuss=""):
    context = {"discusses_page": router.to_path(index)}
    if discuss:
        cmd = discuss_facade.get_discuss_cmd(discuss)
        form = discuss_facade.discuss_form()

        query_discuss = cmd()
        discuss = form.fill_with_model(query_discuss)
        discuss['publisher'] = main_user_form().fill_with_model(MainUser.get_by_id(int(discuss['user'])))

        context['discuss'] = discuss
        return TemplateResponse(template_path="discusses/discuss.html", context=context)
    cmd = discuss_facade.ListDiscussCommand()
    discusses = cmd()
    context['discusses'] = discusses
    return TemplateResponse(context, template_path="discusses/home.html")


def delete(discuss_id):
    discuss_facade.delete_discuss_cmd(discuss_id)()
    return RedirectResponse(router.to_path(index))

