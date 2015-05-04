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
def index():
    return TemplateResponse({'save_path': router.to_path(save)}, 'badges/badge_form.html')


@login_required
def save(**badge_properties):
    cmd = badge_facade.save_badge_cmd(**badge_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'badge': badge_properties}

        return TemplateResponse(context, 'badges/badge_form.html')
    return RedirectResponse(router.to_path(badges))

