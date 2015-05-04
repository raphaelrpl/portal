from gaecookie.decorator import no_csrf
from tekton.gae.middleware.json_middleware import JsonResponse
from recommendation_app.model import Recommendation
from google.appengine.ext import ndb
from question_app.question_model import Question
from discuss_app.discuss_model import Discuss
from gaepermission.decorator import login_required


@login_required
@no_csrf
def index(_logged_user, post_id):
    if _logged_user is None:
        return JsonResponse({"error": "You must be connected"})

    key = ndb.Key(Question, int(post_id))
    post = key.get()
    if post is None:
        key = ndb.Key(Discuss, int(post_id))
        post = key.get()
        if post is None:
            return JsonResponse({"error": "Invalid post"})

    recommend = Recommendation(origin=_logged_user, destination=post)
    recommend.put()

    return JsonResponse({"status": 1})