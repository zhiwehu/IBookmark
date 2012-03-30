from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^/my/import/$', 'bookmark.views.import_bookmark', name='import_bookmark'),
    url(r'^/my/deleteall/$', 'bookmark.views.delete_all_bookmarks', name='delete_all_bookmarks'),
    url(r'^/my/$', 'bookmark.views.my_bookmark', name='my_bookmark'),
    url(r'^/$', 'bookmark.views.bookmark', name='bookmark'),

)