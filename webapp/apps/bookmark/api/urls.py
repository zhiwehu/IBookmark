from piston.resource import Resource
from django.conf.urls.defaults import patterns, url
from authentication import DjangoAuthentication
from handlers import BookmarkHandler
from webapp.apps.bookmark.api.handlers import MyBookmarkHandler

auth = DjangoAuthentication()
bookmark_handler = Resource(BookmarkHandler, authentication=auth)
mybookmark_handler = Resource(MyBookmarkHandler, authentication=auth)

urlpatterns = patterns('',
    url(r'^bookmarks/(?P<bookmark_id>\d+)/$', bookmark_handler, name='api_bookmark'),
    url(r'^bookmarks/my/$', mybookmark_handler, name='api_my_bookmarks'),
    url(r'^bookmarks/$', bookmark_handler, name='api_bookmarks'),
)