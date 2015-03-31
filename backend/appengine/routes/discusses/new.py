# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from discuss_app import discuss_facade
from routes import discusses
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index():
    return TemplateResponse({'save_path': router.to_path(save)}, 'discusss/discuss_form.html')


def save(**discuss_properties):
    cmd = discuss_facade.save_discuss_cmd(**discuss_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'discuss': discuss_properties}

        return TemplateResponse(context, 'discusss/discuss_form.html')
    return RedirectResponse(router.to_path(discusses))

