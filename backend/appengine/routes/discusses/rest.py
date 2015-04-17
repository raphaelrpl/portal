# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from gaecookie.decorator import no_csrf
from tekton.gae.middleware.json_middleware import JsonResponse
from discuss_app import discuss_facade


from google.appengine.api import blobstore
from google.appengine.api.app_identity.app_identity import get_default_gcs_bucket_name
from tekton import router


def index():
    cmd = discuss_facade.list_discusss_cmd()
    discuss_list = cmd()
    discuss_form = discuss_facade.discuss_form()
    discuss_dcts = [discuss_form.fill_with_model(m) for m in discuss_list]
    return JsonResponse(discuss_dcts)


def get_bucket_url():
    from routes.discusses.upload import index as upload_index
    success_url = router.to_path(upload_index)
    bucket = get_default_gcs_bucket_name()
    url = blobstore.create_upload_url(success_url, gs_bucket_name=bucket)
    return url


@no_csrf
def getter():
    output = {"url": get_bucket_url()}
    print(output)
    return JsonResponse(output, secure_prefix="")


@no_csrf
def new(_handler, _resp, **discuss_properties):
    print "DISCUSSS --> "
    print discuss_properties
    cmd = discuss_facade.save_discuss_cmd(**discuss_properties)
    return _save_or_update_json_response(cmd, _resp)


def edit(_resp, id, **discuss_properties):
    print("EDITANO")
    cmd = discuss_facade.update_discuss_cmd(id, **discuss_properties)
    return _save_or_update_json_response(cmd, _resp)


def delete(_resp, id):
    cmd = discuss_facade.delete_discuss_cmd(id)
    try:
        cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)


def _save_or_update_json_response(cmd, _resp):
    try:
        discuss = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    discuss_form = discuss_facade.discuss_form()
    return JsonResponse(discuss_form.fill_with_model(discuss))

