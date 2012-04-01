from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webapp.views.home', name='home'),
    # url(r'^webapp/', include('webapp.foo.urls')),
    url(r'^$', 'bookmark.views.bookmark', name='home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^account/', include('account.urls')),

    url(r'^admin_invite_user/$', 'signup_codes.views.admin_invite_user', name='admin_invite_user'),

    url(r'^social/', include('social_auth.urls')),

    url(r'^about/', include('about.urls')),

    url(r'^setlang', 'django.views.i18n.set_language', name='set_language'),

    url(r'^bookmark', include('bookmark.urls')),

    url(r'^api/', include('bookmark.api.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^site_media/media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
    )
