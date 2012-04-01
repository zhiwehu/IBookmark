from piston.resource import Resource
import json
from django.conf.urls.defaults import patterns, url
from authentication import DjangoAuthentication
from django.http import HttpResponseBadRequest
from handlers import BookmarkHandler, MyBookmarkHandler
from piston.utils import rc

class Resource(Resource):

    def form_validation_response(self, e):
        """
        Turns the error object into a serializable construct.
        All credit for this method goes to Jacob Kaplan-Moss
        """
        return HttpResponseBadRequest(json.dumps(e.form.errors, ensure_ascii=False),
            mimetype="application/json")

auth = DjangoAuthentication()
bookmark_handler = Resource(BookmarkHandler, authentication=auth)
mybookmark_handler = Resource(MyBookmarkHandler, authentication=auth)

urlpatterns = patterns('',
    url(r'^bookmarks/(?P<bookmark_id>\d+)/$', bookmark_handler, name='api_bookmark'),
    url(r'^bookmarks/my/$', mybookmark_handler, name='api_my_bookmarks'),
    url(r'^bookmarks/$', bookmark_handler, name='api_bookmarks'),
)