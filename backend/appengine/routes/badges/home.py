# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from badge_app import badge_facade
from routes.badges import new, edit
from tekton.gae.middleware.redirect import RedirectResponse
from gaepermission.decorator import login_required


@login_required
@no_csrf
def index():
    cmd = badge_facade.list_badges_cmd()
    badges = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    badge_form = badge_facade.badge_form()

    def localize_badge(badge):
        badge_dct = badge_form.fill_with_model(badge)
        badge_dct['edit_path'] = router.to_path(edit_path, badge_dct['id'])
        badge_dct['delete_path'] = router.to_path(delete_path, badge_dct['id'])
        return badge_dct

    localized_badges = [localize_badge(badge) for badge in badges]
    context = {'badges': localized_badges,
               'new_path': router.to_path(new)}
    return TemplateResponse(context, 'badges/badge_home.html')


@login_required
def delete(badge_id):
    badge_facade.delete_badge_cmd(badge_id)()
    return RedirectResponse(router.to_path(index))

