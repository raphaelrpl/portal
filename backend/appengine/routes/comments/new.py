# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from comment_app import comment_facade
from routes import comments
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index():
    return TemplateResponse({'save_path': router.to_path(save)}, 'comments/comment_form.html')


def save(_logged_user, **comment_properties):
    comment_properties['user'] = _logged_user.key.id()
    cmd = comment_facade.save_comment_cmd(**comment_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'comment': comment_properties}

        return TemplateResponse(context, 'comments/comment_form.html')
    return RedirectResponse(router.to_path(comments))

