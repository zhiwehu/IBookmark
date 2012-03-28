from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^/my/$', 'bookmark.views.my_bookmark', name='my_bookmark'),
    url(r'^/$', 'bookmark.views.bookmark', name='bookmark'),

)