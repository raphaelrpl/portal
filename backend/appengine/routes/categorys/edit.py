# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from category_app import category_facade
from routes import categorys
from tekton.gae.middleware.redirect import RedirectResponse
from gaepermission.decorator import login_required


@login_required
@no_csrf
def index(category_id):
    category = category_facade.get_category_cmd(category_id)()
    category_form = category_facade.category_form()
    context = {'save_path': router.to_path(save, category_id), 'category': category_form.fill_with_model(category)}
    return TemplateResponse(context, 'categorys/category_form.html')


@login_required
def save(category_id, **category_properties):
    cmd = category_facade.update_category_cmd(category_id, **category_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors, 'category': category_properties}

        return TemplateResponse(context, 'categorys/category_form.html')
    return RedirectResponse(router.to_path(categorys))

