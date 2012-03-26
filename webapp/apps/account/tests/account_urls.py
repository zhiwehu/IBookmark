from django.conf.urls.defaults import *


urlpatterns = patterns("",
    url(r"^account/", include("urls")),
    url(r"^$", "views.login", name="home") #need a home to correctly render the template..
)
