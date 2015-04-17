# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api.app_identity.app_identity import get_default_gcs_bucket_name
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from discuss_app import discuss_facade
from routes import discusses
from tekton.gae.middleware.redirect import RedirectResponse
from google.appengine.api import blobstore


def get_bucket_url():
    from routes.discusses.upload import index as upload_index
    success_url = router.to_path(upload_index)
    bucket = get_default_gcs_bucket_name()
    url = blobstore.create_upload_url(success_url, gs_bucket_name=bucket)
    return url


@no_csrf
def index():
    upload_path = get_bucket_url()
    return TemplateResponse({'save_path': router.to_path(save), 'upload_url': upload_path}, 'discusss/discuss_form.html')


def save(**discuss_properties):
    cmd = discuss_facade.save_discuss_cmd(**discuss_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'discuss': discuss_properties}

        return TemplateResponse(context, 'discusss/discuss_form.html')
    return RedirectResponse(router.to_path(discusses))

