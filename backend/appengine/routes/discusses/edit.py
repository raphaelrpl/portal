# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from discuss_app import discuss_facade
from routes import discusses
from tekton.gae.middleware.redirect import RedirectResponse
from gaepermission.decorator import login_required


@login_required
@no_csrf
def index(discuss_id):
    discuss = discuss_facade.get_discuss_cmd(discuss_id)()
    discuss_form = discuss_facade.discuss_form()
    context = {'save_path': router.to_path(save, discuss_id), 'discuss': discuss_form.fill_with_model(discuss)}
    return TemplateResponse(context, 'discusss/discuss_form.html')


@login_required
def save(discuss_id, **discuss_properties):
    cmd = discuss_facade.update_discuss_cmd(discuss_id, **discuss_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors, 'discuss': discuss_properties}

        return TemplateResponse(context, 'discusss/discuss_form.html')
    return RedirectResponse(router.to_path(discusses))

