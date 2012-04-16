from django.conf.urls.defaults import patterns, url
from feed import BookmarkFeed
#import message
#from utils import update_bk_screen_shot

urlpatterns = patterns('',
    url(r'^/my/import/$', 'bookmark.views.import_bookmark', name='import_bookmark'),
    url(r'^/my/deleteall/$', 'bookmark.views.delete_all_bookmarks', name='delete_all_bookmarks'),
    url(r'^/my/export/$', 'bookmark.views.export_bookmark', name='export_bookmark'),
    url(r'^/my/$', 'bookmark.views.my_bookmark', name='my_bookmark'),
    url(r'^/$', 'bookmark.views.bookmark', name='bookmark'),
    url(r'^/tag/my/$', 'bookmark.views.my_tag', name='my_tag'),
    url(r'^/tag/$', 'bookmark.views.tag', name='tag'),
    url(r'^/rss/$', BookmarkFeed(), name='rss'),

)

#message.sub('update_bk_screen_shot', update_bk_screen_shot)

import cron