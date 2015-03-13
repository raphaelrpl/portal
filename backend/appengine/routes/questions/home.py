# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from question_app import question_facade
from routes.questions import new, edit
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index():
    cmd = question_facade.list_questions_cmd()
    questions = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    question_form = question_facade.question_form()

    def localize_question(question):
        question_dct = question_form.fill_with_model(question)
        question_dct['edit_path'] = router.to_path(edit_path, question_dct['id'])
        question_dct['delete_path'] = router.to_path(delete_path, question_dct['id'])
        return question_dct

    localized_questions = [localize_question(question) for question in questions]
    context = {'questions': localized_questions,
               'new_path': router.to_path(new)}
    return TemplateResponse(context, 'questions/question_home.html')


def delete(question_id):
    question_facade.delete_question_cmd(question_id)()
    return RedirectResponse(router.to_path(index))

