# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from routes.discusses import download
from discuss_app import discuss_facade
from tekton.gae.middleware.redirect import RedirectResponse
from routes import home


def index(_handler, **discuss_properties):
    blob_infos = _handler.get_uploads("files[]")
    blob_key = blob_infos[0].key()
    avatar = router.to_path(download, blob_key)
    discuss_properties["avatar"] = avatar
    discuss_properties.pop("files", None)
    cmd = discuss_facade.save_discuss_cmd(**discuss_properties)
    try:
        cmd()
    except CommandExecutionException:
        return TemplateResponse(template_path="discusses/home.html")
    return RedirectResponse(router.to_path(home))