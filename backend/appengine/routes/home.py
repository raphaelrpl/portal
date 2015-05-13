# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from permission_app.permission_facade import main_user_form
from question_app import question_facade
from datetime import datetime
from gaepermission.model import MainUser
from tekton import router
from routes.comments.rest import new as comment_path
from discuss_app import discuss_facade
from gaepermission.decorator import login_required

allowed = "python business-intelligence geo-technology mongodb c++ agile artificial-intelligence scidb".split()
from google.appengine.api import blobstore
from google.appengine.api.app_identity.app_identity import get_default_gcs_bucket_name
from routes.discusses.upload import index as my_upload

from category_app.category_model import Category
from question_app.question_model import CategoryQuestion
from discuss_app.discuss_model import CategoryDiscuss
from json import dumps as json_dumps


def get_the_user(model, facade_form):
    model_dct = facade_form.fill_with_model(model)
    model_dct['user'] = MainUser.get_by_id(int(model.user.id()))
    model.created_at = datetime.now() - model.creation
    return model_dct


@login_required
@no_csrf
def index(category=""):
    success_url = router.to_path(my_upload)
    bucket = get_default_gcs_bucket_name()
    url = blobstore.create_upload_url(success_url, gs_bucket_name=bucket)

    topics = [
        {
            "key": 54323122,
            "title": "Who Invented the Computer Virus?",
            "content": "",
            "image": "/static/img/python.jpg",
            "type": "questions",
            "user": 1235875214
        },
        {
            "key": 65432322,
            "title": "How to Google Something You Don't Know How to Describe?",
            "content": "",
            "image": "/static/img/test.jpg",
            "type": "discusses",
            "user": 54389754354
        }
    ]

    if category:
        categ = Category.query(Category.slug == category).fetch()

        if not categ:
            return TemplateResponse(template_path="base/404.html")

        ds = CategoryDiscuss.query(CategoryDiscuss.origin == categ[0].key).fetch()

        dform = discuss_facade.discuss_form()

        doutput = []

        qs = CategoryQuestion.query(CategoryQuestion.origin == categ[0].key).fetch()
        # if category not in allowed:
        qform = question_facade.question_form()

        qoutput = []
        for q in qs:
            question = q.destination.get()
            dct = get_the_user(question, qform)
            dct["type"] = "Q"
            qoutput.append(dct)

        for d in ds:
            discuss = d.destination.get()
            # doutput.append(get_the_user(discuss, dform))
            dct = get_the_user(discuss, dform)
            dct["type"] = "D"
            qoutput.append(dct)
        # "topics": topics,
        context = {"category": categ[0].name,  "topics": qoutput}
        return TemplateResponse(context=context, template_path="category/home.html")
    cmd = question_facade.list_questions_cmd()
    questions = cmd()
    qform = question_facade.question_form()
    main_uform = main_user_form()

    def localize_user(model, facade_form):
        model_dct = facade_form.fill_with_model(model)
        model_dct['user'] = main_uform.fill_with_model(MainUser.get_by_id(int(model.user.id())))
        model.created_at = datetime.now() - model.creation
        return model_dct

    questions_output = [localize_user(q, qform) for q in questions]

    cmd_discuss = discuss_facade.list_discusss_cmd()
    discusses = cmd_discuss()
    dform = discuss_facade.discuss_form()

    discusses_output = [localize_user(d, dform) for d in discusses]

    categorys = Category.query().fetch()

    context = {
        "questions": json_dumps(questions_output),
        "question_comment_path": router.to_path(comment_path),
        "discuss_comment_path": router.to_path(comment_path),
        "users_path": router.to_path(index),
        "upload_path": url,
        "trends": topics,
        "discusses": json_dumps(discusses_output),
        "categorys": categorys
    }
    return TemplateResponse(context=context)

