# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse

from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required
from tekton import router
from routes.discusses import download

from discuss_app.discuss_model import Discuss, CategoryDiscuss
from tekton.gae.middleware.redirect import RedirectResponse
from routes.discusses import home
from category_app.category_model import Category


@login_required
@no_csrf
def index(_handler, _logged_user, **discuss_properties):
    if discuss_properties.get("image"):
        blob_infos = _handler.get_uploads("image[]")
        blob_key = blob_infos[0].key()
        avatar = router.to_path(download, blob_key)
        print(blob_key)
        discuss_properties["image"] = avatar
    discuss_properties["user"] = _logged_user.key
    categorys = discuss_properties.get('categorys')
    try:
        discuss_properties.pop('categorys')
    except:
        pass

    discuss = Discuss(**discuss_properties)

    try:
        discuss.put()

        for category in categorys:
            cat = Category.query(Category.name == category).fetch()
            if cat:
                category = CategoryDiscuss(origin=cat[0], destination=discuss)
                category.put()
        # out = Discuss.get_by_id(discuss.key.id())
        # out.image = avatar
        # out.put()
        print("foi")
    except Exception as e:
        return TemplateResponse(template_path="discusses/home.html")
    return RedirectResponse(router.to_path(home))