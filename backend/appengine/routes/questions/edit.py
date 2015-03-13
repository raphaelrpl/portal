# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from question_app import question_facade
from routes import questions
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index(question_id):
    question = question_facade.get_question_cmd(question_id)()
    question_form = question_facade.question_form()
    context = {'save_path': router.to_path(save, question_id), 'question': question_form.fill_with_model(question)}
    return TemplateResponse(context, 'questions/question_form.html')


def save(question_id, **question_properties):
    cmd = question_facade.update_question_cmd(question_id, **question_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors, 'question': question_properties}

        return TemplateResponse(context, 'questions/question_form.html')
    return RedirectResponse(router.to_path(questions))

