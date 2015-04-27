# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton import router
from routes.discusses import download
from discuss_app import discuss_facade
from discuss_app.discuss_model import Discuss
from tekton.gae.middleware.redirect import RedirectResponse
from routes.discusses import home



@login_not_required
@no_csrf
def index(_handler, _logged_user, **discuss_properties):
    print(100000000)
    print(discuss_properties)
    if discuss_properties.get("image"):
        print(100000000222)
        blob_infos = _handler.get_uploads("image[]")
        print(1000000001345)
        blob_key = blob_infos[0].key()
        avatar = router.to_path(download, blob_key)
        print(blob_key)
        discuss_properties["image"] = avatar
    discuss_properties["user"] = _logged_user.key
    discuss = Discuss(**discuss_properties)

    try:
        discuss.put()
        # out = Discuss.get_by_id(discuss.key.id())
        # out.image = avatar
        # out.put()
        print("foi")
    except Exception as e:
        return TemplateResponse(template_path="discusses/home.html")
    return RedirectResponse(router.to_path(home))