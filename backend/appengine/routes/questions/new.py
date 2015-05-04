# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from question_app import question_facade
from routes import questions
from tekton.gae.middleware.redirect import RedirectResponse
from gaepermission.decorator import login_required


@login_required
@no_csrf
def index():
    return TemplateResponse({'save_path': router.to_path(save)}, 'questions/question_form.html')


@login_required
def save(**question_properties):
    cmd = question_facade.save_question_cmd(**question_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'question': question_properties}

        return TemplateResponse(context, 'questions/question_form.html')
    return RedirectResponse(router.to_path(questions))

