# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from category_app import category_facade
from routes.categorys import edit
from tekton.gae.middleware.redirect import RedirectResponse
from gaebusiness.business import CommandExecutionException
from category_app.category_model import Category
from google.appengine.ext import ndb


@no_csrf
def index():
    cmd = category_facade.list_categorys_cmd()
    categorys = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    category_form = category_facade.category_form()

    def localize_category(category):
        category_dct = category_form.fill_with_model(category)
        category_dct['edit_path'] = router.to_path(edit_path, category_dct['id'])
        category_dct['delete_path'] = router.to_path(delete_path, category_dct['id'])
        return category_dct

    localized_categorys = [localize_category(category) for category in categorys]
    context = {'categorys': localized_categorys,
               'save_path': router.to_path(save),
               'errors': None}
    return TemplateResponse(context, 'categorys/category_home.html')


@no_csrf
def save(**category_properties):
    if Category.is_available_slug(category_properties.get('slug')) != 0:
        category_properties['slug'] = None
    cmd = category_facade.save_category_cmd(**category_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'category': category_properties,
                   'save_path': router.to_path(save)}

        return TemplateResponse(context, 'categorys/category_home.html')
    return RedirectResponse(router.to_path(index))


def delete(category_id):
    # category = Category.get_by_id(int(category_id))
    # category.key.delete()
    category_facade.delete_category_cmd(int(category_id))
    return RedirectResponse(router.to_path(index))

