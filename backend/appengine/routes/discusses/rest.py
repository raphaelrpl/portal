# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from discuss_app.discuss_model import Discuss
from gaebusiness.business import CommandExecutionException
from gaecookie.decorator import no_csrf
from permission_app.permission_facade import main_user_form
from tekton.gae.middleware.json_middleware import JsonResponse
from discuss_app import discuss_facade
from gaepermission.decorator import login_required


from google.appengine.api import blobstore
from google.appengine.api.app_identity.app_identity import get_default_gcs_bucket_name
from tekton import router


@login_required
@no_csrf
def index():
    cmd = discuss_facade.list_discusss_cmd()
    discuss_list = cmd()
    discuss_form = discuss_facade.discuss_form()

    def localize_user(model):
        dct = discuss_form.fill_with_model(model)
        user = main_user_form().fill_with_model(model.user.get())
        dct['user'] = user
        return dct

    discuss_dcts = [localize_user(m)for m in discuss_list]
    return JsonResponse(discuss_dcts)


def get_bucket_url():
    from routes.discusses.upload import index as upload_index
    success_url = router.to_path(upload_index)
    bucket = get_default_gcs_bucket_name()
    url = blobstore.create_upload_url(success_url, gs_bucket_name=bucket)
    return url


@login_required
@no_csrf
def getter():
    output = {"url": get_bucket_url()}
    print(output)
    return JsonResponse(output, secure_prefix="")


@login_required
@no_csrf
def new(_handler, _resp, **discuss_properties):
    print "DISCUSSS --> "
    print discuss_properties
    cmd = discuss_facade.save_discuss_cmd(**discuss_properties)
    return _save_or_update_json_response(cmd, _resp)


@login_required
def edit(_resp, _logged_user, id, **discuss_properties):
    print("EDITANO")
    if 'image' in discuss_properties:
        discuss_properties.pop('image')
    discuss = Discuss.get_by_id(int(id))
    if int(_logged_user.key.id()) != int(discuss_properties.get('user', {}).get('id', 0)):
        _resp.status_code = 400
        return JsonResponse({"content": "This post don't belong to you!"})
    if discuss is None:
        _resp.status_code = 400
        return JsonResponse({"content": "Invalid post"})

    discuss.title = discuss_properties.get('title')
    discuss.content = discuss_properties.get('content')
    try:
        discuss.put()
    except:
        _resp.status_code = 400
        return JsonResponse({"title": "Put a valid title", "content": "Put a valid content"})
    user_form = main_user_form()
    form = discuss_facade.discuss_form()
    discuss_dct = form.fill_with_model(discuss)
    discuss_dct['user'] = user_form.fill_with_model(discuss.user.get())
    return JsonResponse(discuss_dct)


@login_required
def delete(_resp, id):
    cmd = discuss_facade.delete_discuss_cmd(id)
    try:
        discuss = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    discuss_dct = discuss_facade.discuss_form().fill_with_model(discuss)
    return JsonResponse(discuss_dct)


def _save_or_update_json_response(cmd, _resp):
    try:
        discuss = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    discuss_form = discuss_facade.discuss_form()
    return JsonResponse(discuss_form.fill_with_model(discuss))

