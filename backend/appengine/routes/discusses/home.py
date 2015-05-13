# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from comment_app import comment_facade
from comment_app.comment_model import Comment
from config.template_middleware import TemplateResponse
from gaepermission.model import MainUser
from permission_app.permission_facade import main_user_form
from tekton import router
from gaecookie.decorator import no_csrf
from discuss_app import discuss_facade
from tekton.gae.middleware.redirect import RedirectResponse
from routes.comments.rest import delete as comment_delete, new as comment_new
from gaepermission.decorator import login_required
from datetime import datetime
import json


@login_required
@no_csrf
def index(discuss=""):
    context = {"discusses_page": router.to_path(index)}

    def localize_user(model, facade_form):
        model_dct = facade_form.fill_with_model(model)
        model_dct['user'] = main_uform.fill_with_model(MainUser.get_by_id(int(model.user.id())))
        model.created_at = datetime.now() - model.creation
        return model_dct

    if discuss:
        cmd = discuss_facade.get_discuss_cmd(discuss)
        form = discuss_facade.discuss_form()

        query_discuss = cmd()
        if not query_discuss:
            return RedirectResponse(index)
        discuss = form.fill_with_model(query_discuss)

        comment_form = comment_facade.comment_form()
        comments_on_question = Comment.filter_by_question_key(query_discuss.key).fetch()

        def fill_comment_model(comment):
            comment_dct = comment_form.fill_with_model(comment)
            comment_dct['delete_path'] = router.to_path(router.to_path(comment_delete), comment_dct['id'])
            comment_dct['publisher'] = main_user_form().fill_with_model(MainUser.get_by_id(int(discuss['user'])))
            return comment_dct

        comments = [fill_comment_model(c) for c in comments_on_question]

        discuss['user'] = main_user_form().fill_with_model(MainUser.get_by_id(int(discuss['user'])))

        context['discuss'] = discuss
        context['discusses'] = json.dumps([discuss])
        context['comments'] = json.dumps(comments)
        context["comment_url"] = router.to_path(comment_new)
        return TemplateResponse(template_path="discusses/discuss.html", context=context)
    cmd = discuss_facade.ListDiscussCommand()
    discusses = cmd()

    main_uform = main_user_form()
    form = discuss_facade.discuss_form()

    discusses_dct = [localize_user(d, form) for d in discusses]

    context['discusses'] = json.dumps(discusses_dct[::-1])
    return TemplateResponse(context, template_path="discusses/home.html")


@login_required
def delete(discuss_id):
    discuss_facade.delete_discuss_cmd(discuss_id)()
    return RedirectResponse(router.to_path(index))

