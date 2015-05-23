# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from question_app import question_facade
from routes.questions import new, edit
from tekton.gae.middleware.redirect import RedirectResponse
from gaepermission.model import MainUser
from datetime import datetime
from routes.comments.rest import new as comment_new, index as comment_list, delete as comment_delete
from comment_app import comment_facade
from comment_app.comment_model import Comment
from permission_app.permission_facade import main_user_form
from json import dumps
from gaepermission.decorator import login_required


@login_required
@no_csrf
def index(question_id=""):
    main_uform = main_user_form()
    if question_id:
        cmd = question_facade.get_question_cmd(question_id)
        question = cmd()
        form = question_facade.question_form()
        if not question:
            return RedirectResponse(index)
        question_dct = form.fill_with_model(question)
        question_dct['user'] = main_uform.fill_with_model(MainUser.get_by_id(question_dct['user']))

        context = {
            "question": question_dct,
            "questions": dumps([question_dct]),
            "comment_url": router.to_path(comment_new),
            "comment_list": router.to_path(comment_list)}
        return TemplateResponse(context=context, template_path='questions/question.html')
    return TemplateResponse(template_path='questions/home.html')


@login_required
def delete(question_id):
    question_facade.delete_question_cmd(question_id)()
    return RedirectResponse(router.to_path(index))

