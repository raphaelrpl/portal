# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from comment_app import comment_facade
from routes.comments import new, edit
from tekton.gae.middleware.redirect import RedirectResponse
from gaepermission.decorator import login_required


@login_required
@no_csrf
def index():
    cmd = comment_facade.list_comments_cmd()
    comments = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    comment_form = comment_facade.comment_form()

    def localize_comment(comment):
        comment_dct = comment_form.fill_with_model(comment)
        comment_dct['edit_path'] = router.to_path(edit_path, comment_dct['id'])
        comment_dct['delete_path'] = router.to_path(delete_path, comment_dct['id'])
        return comment_dct

    localized_comments = [localize_comment(comment) for comment in comments]
    context = {'comments': localized_comments,
               'new_path': router.to_path(new)}
    return TemplateResponse(context, 'comments/comment_home.html')


@login_required
def delete(comment_id):
    comment_facade.delete_comment_cmd(comment_id)()
    return RedirectResponse(router.to_path(index))

