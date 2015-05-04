# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from badge_app import badge_facade
from routes import badges
from tekton.gae.middleware.redirect import RedirectResponse
from gaepermission.decorator import login_required


@login_required
@no_csrf
def index(badge_id):
    badge = badge_facade.get_badge_cmd(badge_id)()
    badge_form = badge_facade.badge_form()
    context = {'save_path': router.to_path(save, badge_id), 'badge': badge_form.fill_with_model(badge)}
    return TemplateResponse(context, 'badges/badge_form.html')


@login_required
def save(badge_id, **badge_properties):
    cmd = badge_facade.update_badge_cmd(badge_id, **badge_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors, 'badge': badge_properties}

        return TemplateResponse(context, 'badges/badge_form.html')
    return RedirectResponse(router.to_path(badges))

