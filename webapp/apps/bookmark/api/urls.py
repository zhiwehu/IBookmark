from piston.resource import Resource
from django.conf.urls import patterns, url
from authentication import DjangoAuthentication
from handlers import BookmarkHandler

auth = DjangoAuthentication()
bookmark_handler = Resource(BookmarkHandler, authentication=auth)

urlpatterns = patterns('',
    url(r'^bookmarks/(?P<bookmark_id>\d+)/$', bookmark_handler, name='api_bookmark'),
    url(r'^bookmarks/$', bookmark_handler, name='api_bookmarks'),
)